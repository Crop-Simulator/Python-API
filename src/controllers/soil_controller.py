class SoilController:
    def __init__(self):
        self.soil_type = None
        self.precipitation = None
        self.temperature = None

    def input_data(self, soil_type, precipitation, temperature):
        self.soil_type = soil_type
        self.precipitation = precipitation
        self.temperature = temperature

    def calculate_soil_conditions(self):

        if self.soil_type == "sandy":
            moisture_content_in_soil = 0.05 * self.precipitation - 0.01 * self.temperature
            ph_level_in_soil = 6.0
        elif self.soil_type == "loamy":
            moisture_content_in_soil = 0.07 * self.precipitation - 0.01 * self.temperature
            ph_level_in_soil = 6.5
        elif self.soil_type == "clay":
            moisture_content_in_soil = 0.09 * self.precipitation - 0.01 * self.temperature
            ph_level_in_soil = 7.0
        else:
            # If there is no matching soil type, return the default value
            moisture_content_in_soil = 0.0
            ph_level_in_soil = 7.0

        return {"moisture_content_in_soil": moisture_content_in_soil, "ph_level_in_soil": ph_level_in_soil}
