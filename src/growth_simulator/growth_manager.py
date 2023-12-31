import enum
import random


class CropHealth(enum.Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEAD = "dead"

class GrowthManager():
    IRRADIANCE_THRESHOLD = 250
    LOW_IRRADIANCE_DAYS_LIMIT = 5
    PRECIPITATION_THRESHOLD = 0.1
    MIN_TEMPERATURE_THRESHOLD = 37.9 #0 degrees

    def __init__(self, config, model, barley, weather_data):

        self.stage = 0
        self.gdd = 0
        self.barley = barley
        self.model = model
        self.name = self.model.name
        self.config = config["growth_simulator"]
        self.gdd_per_stage = self.config["gdd"]
        self.growth_coefficient = self.config["growth_coefficient"]
        self.p_progression = self.config["p_progression"]
        self.days_per_stage = self.config["days_per_stage"]
        self.effect_of_irradiance = self.config["effect_of_irradiance"]
        self.effect_of_temperature = self.config["effect_of_temperature"]
        self.effect_of_precipitation = self.config["effect_of_precipitation"]
        self.effect_of_weeds = self.config["effect_of_weeds"]

        self.weather_data = weather_data
        self.status = CropHealth.HEALTHY.value
        self.days_passed_since_last_stage = 0

        self.days_high_temperature = 0
        self.days_low_irradiance = 0
        self.days_total_precipitation = 0
        self.current_day = 0
        self.health_points = 10
        self.zero_degrees_celsius = 86

    def progress_day(self):
        self.current_day += 1

    def calculate_growth_degree_days(self, t_max, t_min):
        # barley varieties required an average accumulation of 139 GDD
        # to progress to next stage
        t_base = 0                  # celsius, can be fahrenheit
        gdd = (t_max - t_min)/2 - t_base
        self.gdd += gdd

    def stochastic_growth(self, days_passed):
        if self.barley.health != CropHealth.DEAD.value:
            weed_threshold = len(self.barley.get_weeds()) * self.effect_of_weeds
            growth_threshold = days_passed * self.days_per_stage * self.growth_coefficient/(weed_threshold + 1)
            progression_probability = random.randint(0, self.days_per_stage) < growth_threshold
            return progression_probability #if return 1, progress, else no progress
        else:
            return False

    def progress_stage(self):
        self.calculate_growth_degree_days(self.weather_data[self.current_day]["max_temperature"],
                                          self.weather_data[self.current_day]["min_temperature"])
        can_grow = self.stochastic_growth(self.days_passed_since_last_stage)
        self.days_passed_since_last_stage += 1

        # only grow if reached growth degree days and not at final stage
        # and has reached growth day probability
        max_stages = 10
        if can_grow and self.gdd >= self.gdd_per_stage and self.stage < max_stages:
            self.stage += 1
            self.days_passed_since_last_stage = 0
        return self.stage

    def evaluate_plant_health(self):
        data = self.weather_data[self.current_day]
        if int(float(data["irradiance"])) < self.IRRADIANCE_THRESHOLD:
            self.days_low_irradiance += 1
        else:
            self.days_low_irradiance = 0

        self.days_total_precipitation += int(float(data["precipitation"]))

        if self.days_low_irradiance >= self.LOW_IRRADIANCE_DAYS_LIMIT:
            self.health_points -= self.effect_of_irradiance

        if (self.days_total_precipitation < self.PRECIPITATION_THRESHOLD or
            self.weather_data[self.current_day]["max_temperature"] > self.zero_degrees_celsius or
            self.weather_data[self.current_day]["min_temperature"] < self.MIN_TEMPERATURE_THRESHOLD):

            if self.weather_data[self.current_day]["max_temperature"] > self.zero_degrees_celsius:
                self.days_high_temperature += 1
            if self.days_total_precipitation < self.PRECIPITATION_THRESHOLD:
                self.days_total_precipitation += 1
            self.health_points -= self.effect_of_temperature + self.effect_of_precipitation

        elif self.days_total_precipitation >= self.PRECIPITATION_THRESHOLD:
            self.health_points += self.effect_of_precipitation
        elif random.getrandbits(1) == 1:
                self.health_points += 0.1
        return self.status

    def update_health_status(self):
        low_health = 5
        if self.health_points <= 0:
            self.status = CropHealth.DEAD.value
        elif self.health_points <= low_health:
            self.status = CropHealth.UNHEALTHY.value
        else:
            self.status = CropHealth.HEALTHY.value
        return self.status
