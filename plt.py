import matplotlib

matplotlib.use('Agg')  # 使用Agg后端
import matplotlib.pyplot as plt
import xarray as xr
import numpy as np
import os
import cartopy.crs as ccrs
# import cartopy.io.shapereader as shpreader
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.colors as col
import warnings

warnings.filterwarnings('ignore')


def plot_wind(data, save_path, cmap, levels, two_flag=False):
    le = [2, 5, 9]
    for i in le:
        u = data.u[i].data
        v = data.v[i].data
        r = data.dbz[i].data
        vol = data.vol[i].data

        mask_u = np.where(data.mask[i] == 1, np.nan, u)
        mask_v = np.where(data.mask[i] == 1, np.nan, v)

        lat = data.lat.data
        lon = data.lon.data

        box = [78.5, 82.5, 39.5, 42.5]
        xstep, ystep = 1, 1
        plt.rcParams['font.family'] = 'Times New Roman'
        fig = plt.figure(figsize=(10, 6))
        proj = ccrs.PlateCarree()
        ax = plt.subplot(projection=proj)

        # 显示中国地图
        # province = shpreader.Reader(r'G:\other\all_projection\Wind_Retrieve\City\CN_city.shp')
        # ax.add_geometries(province.geometries(), crs=ccrs.PlateCarree(), linewidths=0.5, edgecolor='k', facecolor='none')
        ax.set_extent(box, crs=ccrs.PlateCarree())
        ax.set_xticks(np.arange(box[0], box[1] + xstep, xstep), crs=ccrs.PlateCarree())
        ax.set_yticks(np.arange(box[2], box[3] + ystep, ystep), crs=ccrs.PlateCarree())
        ax.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label=False))  # 经度0不加标识
        ax.yaxis.set_major_formatter(LatitudeFormatter())
        level = 10
        # cb = ax.contourf(lon, lat, r, transform=ccrs.PlateCarree(), cmap=cmap, levels=levels)
        cb = ax.contourf(lon, lat, transform=ccrs.PlateCarree(), cmap=cmap, levels=levels)
        a, b, c, d = lon[::level, ::level], lat[::level, ::level], u[::level, ::level], v[::level, ::level]
        mask_c, mask_d = mask_u[::level, ::level], mask_v[::level, ::level]
        if two_flag:
            ax.quiver(a, b, mask_c, mask_d, transform=ccrs.PlateCarree(), scale=400, color='k', width=0.002,
                      headwidth=4)
        else:
            ax.quiver(a, b, c, d, transform=ccrs.PlateCarree(), scale=400, color='k', width=0.002, headwidth=4)
        cc = plt.colorbar(cb, orientation='vertical', shrink=1, pad=0.05)
        cc.set_label('dBZ')
        if two_flag:
            plt.savefig(os.path.join(save_path, f'wind_{(i + 1) * 500}_two.png'), dpi=300, bbox_inches='tight')
        else:
            plt.savefig(os.path.join(save_path, f'wind_{(i + 1) * 500}.png'), dpi=300, bbox_inches='tight')
        # plt.show()


save_path = f'D:\\1\\python\\fanyan\\wind_3d\\pic\\25CXW'
levels = np.concatenate([np.array([-20, -5, 0]), np.arange(5, 75, 5)])

cmap = col.ListedColormap(['#7fc2e5', '#00aea5', '#1b20f5', '#40a2f5',
                           '#5becec', '#5ffd10', '#49c60a', '#328f05',
                           '#fefd18', '#e2bf12', '#f48f11', '#f00a0d',
                           '#ca0609', '#b50507', '#f223f0', '#720e84'])

data = xr.open_dataset('wind_data_25CXW.nc')

# two_flag=False代表不考虑至少两部雷达数据的情况，two_flag=True代表考虑至少两部雷达数据的情况
plot_wind(data, save_path, cmap, levels, two_flag=False)
plot_wind(data, save_path, cmap, levels, two_flag=True)
# plot_wind(data, save_path, cmap, levels) # 一部雷达反演图
