# -*- coding: utf-8 -*-
from ywcwr.configure.location_config import atmos_color_path, cloud_color_path
import json


def get_levels_colors(radar_type='atmos', data_type='PDP'):
    """
    :param type:
            Ref dBz,
            ZDR dB,
            KDP °/km,
            Vel m/s,
            SNR dB,
            RHV,
            Wid m/s,
            LDR dB,
            PDP °,
            ......,
    :return:
            levels: colorbar levels
            colors: colorbar colors
            unit: data unit
    """
    levels = []
    colors = []
    if radar_type == 'atmos':
        path = atmos_color_path
    elif radar_type == 'cloud':
        path = cloud_color_path
    data = json.load(open(path, encoding='GBK', mode='r'))[data_type]
    for key, value in data.items():
        levels.append(float(key))
        colors.append(value)

    return levels, colors[1:]

