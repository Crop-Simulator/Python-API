import pandas as pd
from sklearn.linear_model import LinearRegression

class NutrientController:
    def __init__(self, crop_growth_stage, weed_proximity, moisture_content_in_soil, ph_level_in_soil):
        self.crop_growth_stage = crop_growth_stage
        self.weed_proximity = weed_proximity
        self.moisture_content_in_soil = moisture_content_in_soil
        self.ph_level_in_soil = ph_level_in_soil

        # Assume we have a DataFrame `data` with historical data
        data = pd.read_csv("src/controllers/crop_data.csv")  # load data from CSV file

        # Extract the features and targets from historical data
        features = data[["crop_growth_stage", "weed_proximity", "moisture_content_in_soil", "ph_level_in_soil"]]
        water_level_target = data["water_level"]
        nutrient_level_target = data["nutrient_level"]

        # Train the models using historical data
        self.water_level_model = LinearRegression().fit(features, water_level_target)
        self.nutrient_level_model = LinearRegression().fit(features, nutrient_level_target)

    def get_water_level(self):
        # Predict the water level based on current conditions
        input_data = pd.DataFrame([[
            self.crop_growth_stage,
            self.weed_proximity,
            self.moisture_content_in_soil,
            self.ph_level_in_soil,
        ]])
        water_level = self.water_level_model.predict(input_data)
        return water_level[0]

    def get_nutrient_level(self):
        # Predict the nutrient level based on current conditions
        input_data = pd.DataFrame([[
            self.crop_growth_stage,
            self.weed_proximity,
            self.moisture_content_in_soil,
            self.ph_level_in_soil,
        ]])
        nutrient_level = self.nutrient_level_model.predict(input_data)
        return nutrient_level[0]


