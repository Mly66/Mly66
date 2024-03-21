import warnings
warnings.filterwarnings('ignore')
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import numpy as np
from scipy.interpolate import griddata
from ywcwr.configure.default_config import get_metadata
from ywcwr.io import read_auto
from netCDF4 import Dataset
from Variation_3D.core.transforms import geographic_to_cartesian_aeqd, cartesian_to_geographic_aeqd
from Variation_3D import initialization, retrieval, map, retrieve, filters, correct


def del_radar_data(radar_file):
    # 读取雷达数据
    radar = read_auto(radar_file, isfile=True)
    # 转为pyart雷达对象
    radialRadar = radar.PyartRadar
    vel_texture = retrieve.calculate_velocity_texture(radialRadar, vel_field='velocity', wind_size=3)  # 导出速度场
    radialRadar.add_field('velocity_texture', vel_texture, replace_existing=True)  # 添加字段

    gatefilter = filters.GateFilter(radialRadar)  # 构建布尔数组
    gatefilter.exclude_transition()
    gatefilter.exclude_invalid('velocity_texture')
    gatefilter.exclude_invalid('reflectivity')
    gatefilter.exclude_outside('reflectivity', -20, 95)
    gatefilter.exclude_outside('velocity', -27, 63)
    dealias_vel = correct.dealias_region_based(radialRadar, gatefilter=gatefilter)  # 多普勒速度去混叠
    radialRadar.add_field('corrected_velocity', dealias_vel)  # 添加字段

    return radialRadar


def base_data(resolution, Radars):
    """

    :param resolution: 水平分辨率
    :param Radars: 多个雷达数据列表
    :return: size, step, grid_origin, lon, lat, start, end, metas
    """
    grid_metas = []
    grid_origins = []
    for radar in Radars:
        grid_origins.append([radar.latitude['data'][0], radar.longitude['data'][0]])  # 投影中心经纬度位置
        lat, lon, alt = radar.get_gate_lat_lon_alt(0)  # 返回经纬度、高度位置
        grid_metas.append([(alt.min(), alt.max()), (lon.min(), lon.max()), (lat.min(), lat.max())])

    grid_origin = np.mean(np.array(grid_origins), axis=0)
    metas = np.array(grid_metas)
    start_x, start_y = geographic_to_cartesian_aeqd(lat=metas[:, 2].min(), lon=metas[:, 1].min(), lat_0=grid_origin[0],
                                                    lon_0=grid_origin[1])  # 方位角等距地理到笛卡尔坐标变换
    end_x, end_y = geographic_to_cartesian_aeqd(lat=metas[:, 2].max(), lon=metas[:, 1].max(), lat_0=grid_origin[0],
                                                lon_0=grid_origin[1])  # 方位角等距地理到笛卡尔坐标变换

    start_x, end_x = int(np.ceil(start_x)), int(np.ceil(end_x))  # 按元素返回输入的上限
    start_y, end_y = int(np.ceil(start_y)), int(np.ceil(end_y))

    # 计算网格大小
    if start_x % resolution != 0:
        start_x = (start_x // resolution) * resolution
    else:
        start_x = start_x
    if start_y % resolution != 0:
        start_y = (start_y // resolution) * resolution
    else:
        start_y = start_y
    if end_x % resolution != 0:
        end_x = ((end_x // resolution) + 1) * resolution
    else:
        end_x = end_x
    if end_y % resolution != 0:
        end_y = ((end_y // resolution) + 1) * resolution
    else:
        end_y = end_y

    # 计算网格大小
    start, end = min(start_x, start_y), max(end_x, end_y)
    size = min(-start, end)
    step = (end - start) // resolution + 1  # 计算步长
    # 创建网格
    x, y = np.meshgrid(np.arange(start, end + resolution, resolution), np.arange(start, end + resolution, resolution))
    # 笛卡尔坐标到方位角等距地理变换
    lon, lat = cartesian_to_geographic_aeqd(x, y, grid_origin[1], grid_origin[0])

    return size, step, grid_origin, lon, lat, start, end, metas


if __name__ == '__main__':
    # 设置分辨率
    resolution = 1000
    # 读取雷达数据
    Radars = [del_radar_data('2023072515X.06V'),
              del_radar_data('2023072515C.06V'),
              del_radar_data('T_RADR_I_ZY405_20230725150409_O_DOR_XY-D_CAP_FMT.bin.bz2')]
    # 获取基础数据
    size, step, grid_origin, Lon, Lat, start, end, metas = base_data(resolution, Radars)
    # 设置投影参数
    grid_projection = {'proj': 'stere', '_include_lon_0_lat_0': True, 'ellps': "WGS84", 'R': 6370997.0}
    # 计算高度
    alt = Radars[0].altitude['data'][0]
    if len(Radars) == 1:
        alt = Radars[0].altitude['data'][0]
    else:
        alt = metas[:, 0].min()
    z_list = (500 - alt, 5000 - alt)
    z_step = 10
    grids = []
    # 创建掩码
    mask_data = np.zeros_like(Lat).astype(int)
    mask_data = np.repeat(mask_data[np.newaxis, ...], z_step, axis=0)
    # 循环雷达数据
    for radar in Radars:
        # 将雷达数据映射到网格
        grid = map.grid_from_radars(
            (radar,),
            grid_shape=(z_step, step, step),
            grid_limits=(z_list, (start, end), (start, end)),
            grid_origin=grid_origin,
            weighting_function='BARNES2',
            grid_projection=grid_projection,
            fields=['reflectivity', 'corrected_velocity'])  # 将雷达映射返回到grid对象的笛卡尔网格
        grids.append(grid)
        # 创建掩码
        mask_data += (~grid.fields['corrected_velocity']['data'].mask).astype(int)
    # 创建掩码
    mask_array = np.ma.masked_less_equal(mask_data, 0).mask
    mask_array_2 = np.ma.masked_less_equal(mask_data, 1).mask
    # 初始化风场
    u_init, v_init, w_init = initialization.make_constant_wind_field(grids[0], vel_field='corrected_velocity')

    # 10,1500,1,0.01,0.01,0.5,0.5,0.5,3500
    # 计算风场 frz需要替换为当天实际的零度层高度
    Grids = retrieval.get_dd_wind_field(grids,
                                        u_init, v_init, w_init,
                                        Co=10, Cm=1500, Cv=1, Ut=0.01, Vt=0.01,
                                        Cx=0.5, Cy=0.5, Cz=0.5,
                                        frz=4800, filter_window=9,
                                        mask_outside_opt=True, upper_bc=1,
                                        wind_tol=0.5, engine='tensorflow')

    # 获取风场数据
    u = np.round(Grids[0].fields['u']['data'].data, decimals=1)
    v = np.round(Grids[0].fields['v']['data'].data, decimals=1)
    w = np.round(Grids[0].fields['w']['data'].data, decimals=1)
    # 获取反射率和速度数据
    dbz = np.round(Grids[0].fields['reflectivity']['data'].data, decimals=1)
    vol = np.round(Grids[0].fields['corrected_velocity']['data'].data, decimals=1)
    # 将缺失值替换为nan
    u = np.where(mask_array == True, np.nan, u)
    v = np.where(mask_array == True, np.nan, v)
    w = np.where(mask_array == True, np.nan, w)
    dbz = np.where(mask_array == True, np.nan, dbz)
    vol = np.where(mask_array == True, np.nan, vol)

    # 创建坐标网格
    x1 = np.arange(u.shape[1])
    y1 = np.arange(u.shape[2])
    xx, yy = np.meshgrid(x1, y1)

    # 获取非缺失值的坐标和对应的数据
    non_nan_indices = np.where(~np.isnan(u[0]))
    x_known = xx[non_nan_indices]
    y_known = yy[non_nan_indices]

    # 创建插值函数
    for i in range(z_step):
        # 创建坐标网格
        u_known = u[i][non_nan_indices]
        v_known = v[i][non_nan_indices]
        w_known = w[i][non_nan_indices]

        u[i] = griddata((x_known, y_known), u_known, (xx, yy), method='linear')
        v[i] = griddata((x_known, y_known), v_known, (xx, yy), method='linear')
        w[i] = griddata((x_known, y_known), w_known, (xx, yy), method='linear')

    # 创建内存保存nc数据
    mem_file = Dataset('wind_data_25CXW.nc', mode='w', format='NETCDF4')
    # 创建纬度
    mem_file.createDimension("level", u.shape[0])
    mem_file.createDimension("x", u.shape[1])
    mem_file.createDimension("y", u.shape[2])
    # 创建变量并赋予相应单位和属性
    level_var = mem_file.createVariable('level', 'i', ('level',), zlib=True)
    level_var.long_name = 'level'
    level_var.units = 'm'

    lat = mem_file.createVariable('lat', 'f', ('x', 'y'), zlib=True)
    lat.long_name = 'latitude'
    lat.units = 'degrees_north'

    lon = mem_file.createVariable('lon', 'f', ('x', 'y'), zlib=True)
    lon.long_name = 'longitude'
    lon.units = 'degrees_east'

    u_var = mem_file.createVariable("u", "f", ("level", "x", "y",), zlib=True)
    u_var.units = 'm/s'

    v_var = mem_file.createVariable("v", "f", ("level", "x", "y",), zlib=True)
    v_var.units = 'm/s'

    w_var = mem_file.createVariable("w", "f", ("level", "x", "y",), zlib=True)
    w_var.units = 'm/s'

    dbz_var = mem_file.createVariable("dbz", "f", ("level", "x", "y",), zlib=True)
    dbz_var.units = 'dBZ'

    vol_var = mem_file.createVariable("vol", "f", ("level", "x", "y",), zlib=True)
    vol_var.units = 'm/s'

    mask_var = mem_file.createVariable("mask", "i", ("level", "x", "y",), zlib=True)

    # 变量赋值
    level_var[:] = np.arange(500, 5000 + 500, 500)
    lat[:] = Lat  # 纬度值
    lon[:] = Lon  # 经度值
    u_var[:, :, :] = u
    v_var[:, :, :] = v
    w_var[:, :, :] = w
    dbz_var[:, :, :] = dbz
    vol_var[:, :, :] = vol
    mask_var[:, :, :] = mask_array_2

    mem_file.real_min_lat = Lat.min()
    mem_file.real_min_lon = Lon.min()
    mem_file.real_max_lat = Lat.max()
    mem_file.real_max_lon = Lon.max()

    mem_file.resolution = resolution
    # 关闭文件
    mem_file.close()
