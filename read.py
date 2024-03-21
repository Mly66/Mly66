import matplotlib
matplotlib.use('Agg')
import os
from tqdm import tqdm
from ywcwr.io import read_auto
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as col
import warnings

warnings.filterwarnings("ignore")

filename = "2023072515X.06V"
# 读取雷达数据
radar = read_auto(filename, isfile=True)
# 查看雷达数据的基本信息
# print(radar.scan_info)
# 查看所有仰角层雷达数据
print(radar.fields)
# 查看第一个仰角层的反射率数据
# print(radar.fields[0]['dBZ'])
# 查看第一个仰角层的速度数据
# print(radar.fields[0]['V'])
# 查看第一个仰角层的谱宽数据
# print(radar.fields[0]['W'])


'''
levels = np.concatenate([np.array([-20, -5, 0]), np.arange(5, 75, 5)])  # 反射率用这个
# levels = np.arange(-12, 13, 3)  # 速度场用这个

cmap = col.ListedColormap(['#7fc2e5', '#00aea5', '#1b20f5', '#40a2f5',
                           '#5becec', '#5ffd10', '#49c60a', '#328f05',
                           '#fefd18', '#e2bf12', '#f48f11', '#f00a0d',
                           '#ca0609', '#b50507', '#f223f0', '#720e84'])
out_path = f'D:\\1\\python\\fanyan\\wind_3d\\jiema pic'
# filename = "T_RADR_I_ZY405_20230727152441_O_DOR_XY-D_CAP_FMT.bin.bz2"
filename = "2023072515X.06V"
radar = read_auto(filename, isfile=True)

for layer in tqdm(range(radar.scan_info.sweep.shape[0])):
    folder = os.path.join(out_path, filename.split('.')[0])
    if not os.path.exists(folder):
        os.makedirs(folder)
    lon = radar.fields[layer]['dBZ']['lon']  # 如果要看反射率就把V改成'dBZ'，下面两个同理
    lat = radar.fields[layer]['dBZ']['lat']
    data = radar.fields[layer]['dBZ'].data

    plt.figure()
    plt.contourf(lon, lat, data, cmap=cmap, levels=levels)
    plt.colorbar()
    plt.savefig(os.path.join(folder, f'{filename}_{layer}.png'), dpi=300, bbox_inches='tight')
    plt.show()
'''