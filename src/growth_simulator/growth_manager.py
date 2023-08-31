import numpy as np
import enum

class CropHealth(enum.Enum):
    HEALTHY = "healthy"
    UNHEALTHY = "unhealthy"
    DEAD = "dead"

class GrowthManager():
    IRRADIANCE_THRESHOLD = 250
    LOW_IRRADIANCE_DAYS_LIMIT = 5
    PRECIPITATION_THRESHOLD = 0.48

    def __init__(self, config, model, days_per_stage):
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
        self.weather_data = []
        self.status = "healthy"
        self.days_low_irradiance = 0
        self.days_total_precipitation = 0
        self.current_day = 0

    def set_weather_data(self, data):
        self.weather_data = data
        
    def progress_day(self):
        self.current_day += 1

    def growth_degree_days(self, t_max, t_min):
        # barley varieties required an average accumulation of 139 GDD
        # to progress to next stage
        t_base = 0                  # celsius, can be fahrenheit
        gdd = (t_max - t_min)/2 - t_base
        self.gdd += gdd

    def growth_binomial_distribution(self, days_passed):
        section = days_passed % self.days_per_stage
        p = self.p_progression * section
        progression_probability = np.random.binomial(1, p)
        return progression_probability # if return 1, progress, else no progress

    def progress_stage(self):
        if self.gdd >= self.GDD_PER_STAGE and self.stage < 10:
            self.stage += 1
            self.model.set_model_stage(self.stage)

    def evaluate_plant_health(self, weather_data, day):
        data = weather_data[day]
        if int(float(data["irradiance"])) < self.IRRADIANCE_THRESHOLD:
            self.days_low_irradiance += 1
        else:
            self.days_low_irradiance = 0

        self.days_total_precipitation += int(float(data["precipitation"]))

        if self.days_low_irradiance >= self.LOW_IRRADIANCE_DAYS_LIMIT:
            self.status = CropHealth.UNHEALTHY
            return self.status
        if self.days_total_precipitation < self.PRECIPITATION_THRESHOLD:
            self.status = CropHealth.DEAD
            return self.status
        return self.status