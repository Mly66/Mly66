"""
Configuration file for the PRD Object , modified from Py-art
注意：距离单位统一到m
"""

FILL_VALUE = -9999.0
_LIGHT_SPEED = 2.99792458e8

DEFAULT_METADATA = {
    # Metadata for radar attributes. These closely follow the CF/Radial
    # standard

    'azimuth': {
        'units': 'degrees',
        'standard_name': 'beam_azimuth_angle',
        'long_name': 'azimuth_angle_from_true_north',
        'axis': 'radial_azimuth_coordinate',
        'comment': 'Azimuth of antenna relative to true north'},

    'elevation': {
        'units': 'degrees',
        'standard_name': 'beam_elevation_angle',
        'long_name': 'elevation_angle_from_horizontal_plane',
        'axis': 'radial_elevation_coordinate',
        'comment': 'Elevation of antenna relative to the horizontal plane'},

    'range': {
        'units': 'meters',
        'standard_name': 'projection_range_coordinate',
        'long_name': 'range_to_measurement_volume',
        'axis': 'radial_range_coordinate',
        'spacing_is_constant': 'true',
        'comment': (
            'Coordinate variable for range. Range to center of each bin.')},

    'time': {
        'standard_name': 'time',
        'long_name': 'time_in_seconds_since_volume_start',
        'calendar': 'gregorian',
        'comment': ('Coordinate variable for time. '
                    'Time at the center of each ray, in fractional seconds '
                    'since the global variable time_coverage_start')},
    'start_time': {
        'standard_name': 'start_time',
        'long_name': 'UTC_time_at_volume_start',
        'calendar': 'gregorian',
        'comment': ('Coordinate variable for time. '
                    'Time at the center of each ray, in fractional seconds '
                    'since the global variable time_coverage_start')},
    'end_time': {
        'standard_name': 'end_time',
        'long_name': 'UTC_time_at_volume_end',
        'calendar': 'gregorian',
        'comment': ('Coordinate variable for time. '
                    'Time at the center of each ray, in fractional seconds '
                    'since the global variable time_coverage_start')},

    'fixed_angle': {
        'long_name': 'Target angle for sweep',
        'units': 'degrees',
        'standard_name': 'target_fixed_angle'},

    'rays_per_sweep': {
        'long_name': 'Number of rays in each sweep',
        'units': 'count'},

    'latitude': {
        'long_name': 'Latitude',
        'standard_name': 'Latitude',
        'units': 'degrees_north'},
    'lat': {
        'long_name': 'Latitude',
        'standard_name': 'Latitude',
        'units': 'degrees_north'},
    'y': {
        'long_name': 'distance from radar in north',
        'standard_name': 'distance in y',
        'units': 'meters'},

    'longitude': {
        'long_name': 'Longitude',
        'standard_name': 'Longitude',
        'units': 'degrees_east'},

    'lon': {
        'long_name': 'Longitude',
        'standard_name': 'Longitude',
        'units': 'degrees_east'},

    'x': {
        'long_name': 'distance from radar in east',
        'standard_name': 'distance in x',
        'units': 'meters'},

    'altitude': {
        'long_name': 'Altitude',
        'standard_name': 'Altitude',
        'units': 'meters',
        'positive': 'up'},
    'z': {
        'long_name': 'sea surface level',
        'standard_name': 'altitude in z',
        'positive': 'up',
        'units': 'meters'},

    'nyquist_velocity': {
        'units': 'meters_per_second',
        'comments': "Unambiguous velocity",
        'meta_group': 'instrument_parameters',
        'long_name': 'Nyquist velocity'},

    'unambiguous_range': {
        'units': 'meters',
        'comments': 'Unambiguous range',
        'meta_group': 'instrument_parameters',
        'long_name': 'Unambiguous range'},
    'frequency': {
        'units': 'GHZ',
        'meta_group': 'instrument_parameters',
        'long_name': 'Radiation frequency'},

    # Reflectivity fields
    'reflectivity': {
        'units': 'dBZ',
        'standard_name': 'equivalent_reflectivity_factor',
        'long_name': 'Reflectivity',
        'cn_name': '基本反射率(Z)',
        'valid_max': 94.5,
        'valid_min': -33.0,
        'coordinates': 'elevation azimuth range'},
    'un_reflectivity': {
        'units': 'dBZ',
        'standard_name': 'equivalent_reflectivity_factor',
        'long_name': 'Unfilter Reflectivity',
        'cn_name': '未滤波反射率(UnZ)',
        'valid_max': 94.5,
        'valid_min': -33.0,
        'coordinates': 'elevation azimuth range'},
    "corrected_reflectivity": {
        'units': 'dBZ',
        'standard_name': 'corrected_equivalent_reflectivity_factor',
        'long_name': 'Corrected reflectivity',
        'cn_name': '退模糊后基本反射率(Z)',
        'valid_max': 94.5,
        'valid_min': -33.0,
        'coordinates': 'elevation azimuth range'},
    'scan_type': {
        'units': "string",
        'standard_name': "radar scan type",
        'long_name': "Type of scan, one of 'ppi', 'rhi', 'sector' or 'other'"
    },
    'total_power': {
        'units': 'dBZ',
        'standard_name': 'equivalent_reflectivity_factor',
        'long_name': 'Total power',
        'valid_max': 80.0,
        'valid_min': -30.0,
        'coordinates': 'elevation azimuth range'},

    # Velocity fields
    'velocity': {
        'units': 'm/s',
        'standard_name': 'radial_velocity_of_scatterers_away_from_instrument',
        'long_name': 'Mean dopper velocity',
        'cn_name': '基本多普勒速度(V)',
        'valid_max': 63.0,
        'valid_min': -63.0,
        'coordinates': 'elevation azimuth range'},

    "corrected_velocity": {
        'units': 'm/s',
        'standard_name': 'corrected_radial_velocity_of_scatterers_away_from_instrument',
        'cn_name': '退模糊后基本多普勒速度(V)',
        'valid_max': 63.0,
        'valid_min': -63.0,
        'long_name': 'Corrected mean doppler velocity',
        'coordinates': 'elevation azimuth range'},

    # Spectrum width fields
    'spectrum_width': {
        'units': 'm/s',
        'standard_name': 'doppler_spectrum_width',
        'long_name': 'Doppler spectrum width',
        'cn_name': '基本普宽(W)',
        'valid_max': 63.0,
        'valid_min': 0.0,
        'coordinates': 'elevation azimuth range'},

    # Dual-polarization fields
    'differential_reflectivity': {
        'units': 'dB',
        'standard_name': 'log_differential_reflectivity_hv',
        'long_name': 'Differential reflectivity',
        'cn_name': '差分反射率(ZDR)',
        'valid_max': 8.0,
        'valid_min': -2.0,
        'coordinates': 'elevation azimuth range'},

    'cross_correlation_ratio': {
        'units': 'ratio',
        'standard_name': 'cross_correlation_ratio_hv',
        'long_name': 'Cross correlation ratio (RHOHV)',
        'cn_name': '零延迟相关系数(RHV or CC)',
        'valid_max': 1.0,
        'valid_min': 0.0,
        'coordinates': 'elevation azimuth range'},

    'normalized_coherent_power': {
        'units': 'ratio',
        'standard_name': 'normalized_coherent_power',
        'long_name': 'Normalized coherent power',
        'valid_max': 1.0,
        'valid_min': 0.0,
        'comment': 'Also know as signal quality index (SQI)',
        'coordinates': 'elevation azimuth range'},

    'differential_phase': {
        'units': 'degrees',
        'standard_name': 'differential_phase_hv',
        'long_name': 'Differential phase (PhiDP)',
        'cn_name': '差分相移(PDP)',
        'valid_max': 360.0,
        'valid_min': 0.0,
        'coordinates': 'elevation azimuth range'},
    'specific_differential_phase': {
        'units': 'degrees/km',
        'standard_name': 'specific_differential_phase_hv',
        'long_name': 'Specific differential phase (KDP)',
        'cn_name': '差分相移率(KDP)',
        'valid_max': 5,
        'valid_min': -2,
        'coordinates': 'elevation azimuth range'},
    'clutter_flag': {
        'standard_name': 'clutter_flag',
    },
    "horizontal_signal_noise_ratio": {
        'standard_name': 'horizontal signal noise ratio',
    },
    "vertical_signal_noise_ratio": {
        'standard_name': 'vertical signal noise_ratio',
    },
    "flag_of_rpv_data": {
        'standard_name': 'flag of rpv data',
    },
    # Depolarization ratio fields
    'linear_depolarization_ratio': {
        'units': 'dB',
        'standard_name': 'log_linear_depolarization_ratio_hv',
        'long_name': 'Linear depolarization ratio',
        'valid_max': 0,
        'valid_min': -40.0,
        'coordinates': 'elevation azimuth range'},
    "clutter_phase_alignment": {
        'units': 'ratio',
        'standard_name': 'clutter_phase_alignment',
        'long_name': 'clutter phase alignment',
        'valid_max': 0,
        'valid_min': 1,
        'coordinates': 'elevation azimuth range'},
    "beam_width": {
        'units': 'degrees',
        'standard_name': 'beam_width_polarization',
        'long_name': 'Antenna beam width polarization',
        'valid_max': 0,
        'valid_min': 5,
        'coordinates': 'sweep'},
    "hydro_class": {
        'cn_name': '粒子相态(HCL)',
        'standard_name': 'hydro_class',
        'unit': "‘0’非气象；‘1’小雨；‘2’中雨；‘3’大雨；‘4’干雪；‘5’湿雪；‘6’冰晶；‘7’小冰雹；‘8’大冰雹；‘9’雨夹雹",
    },
    "signal_to_noise_ratio": {
        'units': 'dB',
        'cn_name': '反射率的信噪比',
        'standard_name': 'signal_to_noise_ratio',
        'long_name': 'signal to noise ratio',
        'valid_max': 94.5,
        'valid_min': -33.0,
    },
    "longutide_wind": {
        'units': 'm/s',
        'standard_name': 'radial_velocity_of_scatterers_away_from_instrument',
        'cn_name': '经度方向速度(U)',
        'valid_max': 63.0,
        'valid_min': -63.0,
        'long_name': 'Corrected mean doppler velocity',
        'coordinates': 'elevation azimuth range'},
    "latitude_wind": {
        'units': 'm/s',
        'standard_name': 'radial_velocity_of_scatterers_away_from_instrument',
        'cn_name': '纬度方向速度(V)',
        'valid_max': 63.0,
        'valid_min': -63.0,
        'long_name': 'Corrected mean doppler velocity',
        'coordinates': 'elevation azimuth range'},
    "altitude_wind": {
        'units': 'm/s',
        'standard_name': 'radial_velocity_of_scatterers_away_from_instrument',
        'cn_name': '高度方向速度(W)',
        'valid_max': 63.0,
        'valid_min': -63.0,
        'long_name': 'Corrected mean doppler velocity',
        'coordinates': 'elevation azimuth range'}
}

# CINRAD files
CINRAD_field_mapping = {
    # moment: radar field name
    'dBT': 'total_power',
    'dBZ': "reflectivity",
    'UnZ': "un_reflectivity",
    'V': "velocity",
    'W': "spectrum_width",
    'SQI': 'normalized_coherent_power',
    'CPA': 'clutter_phase_alignment',
    'ZDR': "differential_reflectivity",
    'LDR': "linear_depolarization_ratio",
    'CC': "cross_correlation_ratio",
    'PhiDP': "differential_phase",
    'KDP': "specific_differential_phase",
    'CP': "clutter_probability",
    'Flag': "flag_of_rpv_data",
    'HCL': "hydro_class",
    'CF': "clutter_flag",
    'Zc': "corrected_reflectivity",
    'Vc': "corrected_velocity",
    'Wc': "spectrum_width_corrected",
    'SNRH': "horizontal_signal_noise_ratio",
    'SNRV': "vertical_signal_noise_ratio",
    'SNR': 'signal_to_noise_ratio',
    'Uwind': 'longutide_wind',
    'Vwind': 'latitude_wind',
    'Wwind': 'altitude_wind',
}

CINRAD_COLORMAP = {
    "reflectivity": 'CN_ref',
    'un_reflectivity': 'CN_ref',
    "corrected_reflectivity": 'CN_ref',
    "total_power": 'CN_ref',
    "signal_to_noise_ratio": 'CN_ref',
    "velocity": 'CN_vel',  # CN_vel pyart_NWSVel
    "corrected_velocity": 'CN_vel',  # pyart_BuDRd18
    "simulated_velocity": 'CN_vel',
    "eastward_wind_component": 'pyart_BuDRd18',
    "northward_wind_component": 'pyart_BuDRd18',
    "vertical_wind_component": 'pyart_BuDRd18',
    "spectrum_width": 'pyart_NWS_SPW',
    "normalized_coherent_power": 'pyart_Carbone17',
    "differential_reflectivity": 'pyart_RefDiff',
    "corrected_differential_reflectivity": 'pyart_RefDiff',
    "cross_correlation_ratio": 'pyart_RefDiff',
    "differential_phase": 'pyart_RefDiff',
    "unfolded_differential_phase": 'pyart_Wild25',
    "corrected_differential_phase": 'pyart_Wild25',
    "specific_differential_phase": 'pyart_RefDiff',
    "corrected_specific_differential_phase": 'pyart_Theodore16',
    "linear_depolarization_ratio": 'pyart_SCook18',
    "linear_depolarization_ratio_h": 'pyart_SCook18',
    "linear_depolarization_ratio_v": 'pyart_SCook18',
    "rain_rate": 'pyart_RRate11',
    "radar_estimated_rain_rate": 'pyart_RRate11',
    "radar_echo_classification": 'pyart_LangRainbow12',
    "specific_attenuation": 'pyart_Carbone17',
    "differential_phase_texture": 'pyart_BlueBrown11',
    "height": 'pyart_SCook18',
    "interpolated_profile": 'pyart_SCook18',
}

CINRAD_field_clevs = {
    "corrected_velocity": [-63, -27, -20, -15, -10, -5, -1,
                           0, 1, 5, 10, 15, 20, 27, 63],
    "velocity": [-63, -27, -20, -15, -10, -5, -1,
                 0, 1, 5, 10, 15, 20, 27, 63],
    "reflectivity": [-20.0, -5.0, 0.0,
                     5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0,
                     45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 94.5],
    "un_reflectivity": [-20.0, -5.0, 0.0,
                     5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0,
                     45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 94.5],
    "velocity_texture": [-63, -27, -20, -15, -10, -5, -1,
                         0, 1, 5, 10, 15, 20, 27, 63],
    "signal_to_noise_ratio": [-20.0, -5.0, 0.0,
                              5.0, 10.0, 15.0, 20.0, 25.0, 30.0, 35.0, 40.0,
                              45.0, 50.0, 55.0, 60.0, 65.0, 70.0, 94.5],
}

CINRAD_field_bins = {
    # moment: radar field name
    'total_power': 16,
    "reflectivity": 18,
    "un_reflectivity": 18,
    "velocity": 15,
    "velocity_texture": 15,
    "spectrum_width": 16,
    'normalized_coherent_power': 16,
    "differential_reflectivity": 16,
    "linear_depolarization_ratio": 16,
    "cross_correlation_ratio": 16,
    "differential_phase": 12,
    "specific_differential_phase": 12,
    "clutter_flag": 16,
    "corrected_reflectivity": 16,
    "corrected_velocity": 15,
    "signal_to_noise_ratio": 18,
    "simulated_velocity": 16,
    "eastward_wind_component": 16,
    "northward_wind_component": 16,
    "vertical_wind_component": 16,
    "corrected_differential_reflectivity": 16,
    "unfolded_differential_phase": 16,
    "corrected_differential_phase": 16,
    "corrected_specific_differential_phase": 16,
    "linear_depolarization_ratio_h": 16,
    "linear_depolarization_ratio_v": 16,
    "rain_rate": 16,
    "radar_estimated_rain_rate": 16,
    "radar_echo_classification": 16,
    "specific_attenuation": 16,
    "differential_phase_texture": 16,
    "height": 16,
    "interpolated_profile": 16,
}

CINRAD_field_normvar = {
    # moment: radar field name
    'total_power': (-5, 75),
    "reflectivity": (-20, 94.5),
    "un_reflectivity": (-20, 94.5),
    "velocity": (-63.5, 63),
    "spectrum_width": (0, 63.0),
    'normalized_coherent_power': -1,
    "differential_reflectivity": (-2, 8),
    "linear_depolarization_ratio": -1,
    "cross_correlation_ratio": (0, 1),
    "differential_phase": (0, 180),
    "specific_differential_phase": (-1, 6),
    "clutter_flag": -1,
    "corrected_reflectivity": (-33, 94.5),
    "corrected_velocity": (-63.5, 63),
    "signal_to_noise_ratio": (-20, 94.5),
    "simulated_velocity": -1,
    "eastward_wind_component": -1,
    "northward_wind_component": -1,
    "vertical_wind_component": -1,
    "corrected_differential_reflectivity": -1,
    "unfolded_differential_phase": -1,
    "corrected_differential_phase": -1,
    "corrected_specific_differential_phase": -1,
    "linear_depolarization_ratio_h": -1,
    "linear_depolarization_ratio_v": -1,
    "rain_rate": -1,
    "radar_estimated_rain_rate": -1,
    "radar_echo_classification": -1,
    "specific_attenuation": -1,
    "differential_phase_texture": -1,
    "height": -1,
    "interpolated_profile": -1,
}


def get_metadata(p):
    """
    Return a dictionary of metadata for a given parameter, p.

    An empty dictionary will be returned in no metadata dictionary exists for
    parameter p.
    """
    if p in DEFAULT_METADATA:
        return DEFAULT_METADATA[p].copy()
    else:
        return {}
