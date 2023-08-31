import numpy as np
import enum
import os


class CropHealth(enum.Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEAD = "dead"

class GrowthManager():
    IRRADIANCE_THRESHOLD = 250
    LOW_IRRADIANCE_DAYS_LIMIT = 5
    PRECIPITATION_THRESHOLD = 0.1

    def __init__(self, config, model, days_per_stage, weather_data):
        self.GDD_PER_STAGE = 139
        self.stage = 0
        self.gdd = 0
        self.model = model
        self.model_stage = self.model.set_model_stage(self.stage)
        self.name = self.model_stage.name
        self.days_per_stage = days_per_stage    # expected number of days per stage
        self.probability_of_success = 0.8       # probability of success on day for that stage
        self.config = config["growth_simulator"]
        self.p_progression = self.config["p_progression"]
        self.days_per_stage = self.config["days_per_stage"]
        self.effect_of_irradiance = self.config["effect_of_irradiance"]
        self.effect_of_temperature = self.config["effect_of_temperature"]
        self.effect_of_precipitation = self.config["effect_of_precipitation"]
        self.weather_data = weather_data
        self.status = "healthy"
        
        self.days_high_temperature = 0
        self.days_low_irradiance = 0
        self.days_total_precipitation = 0
        self.current_day = 0
        self.health_points = 10
    
    def progress_day(self):
        self.current_day += 1

    def calculate_growth_degree_days(self, t_max, t_min):
        # barley varieties required an average accumulation of 139 GDD
        # to progress to next stage
        t_base = 0                  # celsius, can be fahrenheit
        gdd = (t_max - t_min)/2 - t_base
        self.gdd += gdd

    def growth_binomial_distribution(self, days_passed):
        # grows with probability p_progression
        # maximum liklihood of progression at days_per_stage set in data.yml
        section = days_passed % self.days_per_stage
        p = self.p_progression * section
        progression_probability = np.random.binomial(1, p)
        return progression_probability # if return 1, progress, else no progress

    def progress_stage(self):
        self.calculate_growth_degree_days(self.weather_data[self.current_day]["max_temperature"],
                                          self.weather_data[self.current_day]["min_temperature"])
        can_grow = self.growth_binomial_distribution()
        # only grow if reached growth degree days and not at final stage
        # and has reached growth day probability
        if can_grow and self.gdd >= self.GDD_PER_STAGE and self.stage < 10:
            self.stage += 1
            return self.model.set_model_stage(self.stage)

    def evaluate_plant_health(self, weather_data, day):
        data = weather_data[day]
        print(data)
        if int(float(data["irradiance"])) < self.IRRADIANCE_THRESHOLD:
            self.days_low_irradiance += 1
        else:
            self.days_low_irradiance = 0

        self.days_total_precipitation += int(float(data["precipitation"]))

        if self.days_low_irradiance >= self.LOW_IRRADIANCE_DAYS_LIMIT:
            self.health_points -= self.effect_of_irradiance
        if self.days_total_precipitation < self.PRECIPITATION_THRESHOLD or self.weather_data[day]["max_temperature"] > 86:
            if self.weather_data[day]["max_temperature"] > 86:
                self.days_high_temperature += 1
            if self.days_total_precipitation < self.PRECIPITATION_THRESHOLD:
                self.days_total_precipitation += 1
            self.health_points -= self.effect_of_temperature + self.effect_of_precipitation
        elif self.days_total_precipitation >= self.PRECIPITATION_THRESHOLD:
            self.health_points += self.effect_of_precipitation
        return self.status
    
    def simulate_growth(self):
        self.progress_day()
        self.evaluate_plant_health(self.weather_data, self.current_day)
        if self.status== CropHealth.DEAD.value:
            return self.model
        elif self.status == CropHealth.UNHEALTHY.value:
            crop = self.progress_stage()
            return crop
        else:
            return self.model