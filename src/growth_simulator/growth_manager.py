import numpy as np

class GrowthManager():
    def __init__(self, config, model, days_per_stage):
        self.GDD_PER_STAGE = 139
        self.stage = 0
        self.gdd = 0
        self.model = model
        self.model_stage = self.set_model_stage(self.stage)
        self.name = self.model_stage.name
        self.days_per_stage = days_per_stage    # expected number of days per stage
        self.probability_of_success = 0.8       # probability of success on day for that stage
        self.config = config["growth_simulator"]
        self.p_progression = self.config["p_progression"]
        self.days_per_stage = self.config["days_per_stage"]

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
        if self.gdd >= self.GDD_PER_STAGE:
            self.stage += 1
            self.set_model_stage(self.stage)
