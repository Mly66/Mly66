from ywcwr.io.CdywDFile import  CdywDBaseData,YwKa2NRadar


class ChooseData(object):
    def __init__(self, prd_data=None, sweep=None, field_name=None):
        self.prd_data = prd_data
        self.sweep = sweep
        self.field_name = field_name


    def _data_choose(self):
        dims = self.prd_data.scan_info.dims
        coords = self.prd_data.scan_info.coords
        latitude = self.prd_data.scan_info.data_vars["latitude"]
        longitude = self.prd_data.scan_info.data_vars["longitude"]
        altitude = self.prd_data.scan_info.data_vars["altitude"]
        scan_type = self.prd_data.scan_info.data_vars["scan_type"]
        frequency = self.prd_data.scan_info.data_vars["frequency"]
        start_time = self.prd_data.scan_info.data_vars["start_time"]
        end_time = self.prd_data.scan_info.data_vars["end_time"]
        nyquist_velocity = self.prd_data.scan_info.data_vars["nyquist_velocity"][self.sweep]
        unambiguous_range = self.prd_data.scan_info.data_vars["unambiguous_range"][self.sweep]
        polarzation_type = self.prd_data.scan_info.data_vars["polarzation_type"][self.sweep]
        rays_per_sweep = self.prd_data.scan_info.data_vars["rays_per_sweep"][self.sweep]
        fixed_angel = self.prd_data.scan_info.data_vars["fixed_angel"][self.sweep]
        bean_width = self.prd_data.scan_info.data_vars["bean_width"][self.sweep]
        fields = self.prd_data.fields[self.sweep][self.field_name]

        scan_info = {dims: self.prd_data.scan_info.dims,
                     coords: self.prd_data.scan_info.coords,
                     latitude: self.prd_data.scan_info.data_vars["longitude"],
                     longitude: self.prd_data.scan_info.data_vars["longitude"],
                     altitude: self.prd_data.scan_info.data_vars["altitude"],
                     scan_type: self.prd_data.scan_info.data_vars["scan_type"],
                     frequency: self.prd_data.scan_info.data_vars["frequency"],
                     start_time: self.prd_data.scan_info.data_vars["start_time"],
                     end_time: self.prd_data.scan_info.data_vars["end_time"],
                     nyquist_velocity: self.prd_data.scan_info.data_vars["nyquist_velocity"][self.sweep],
                     unambiguous_range: self.prd_data.scan_info.data_vars["unambiguous_range"][self.sweep],
                     polarzation_type: self.prd_data.scan_info.data_vars["polarzation_type"][self.sweep],
                     rays_per_sweep: self.prd_data.scan_info.data_vars["rays_per_sweep"][self.sweep],
                     fixed_angel: self.prd_data.scan_info.data_vars["fixed_angel"][self.sweep],
                     bean_width: self.prd_data.scan_info.data_vars["bean_width"][self.sweep],
                     }

        fields = self.prd_data.fields[self.sweep][self.field_name]
