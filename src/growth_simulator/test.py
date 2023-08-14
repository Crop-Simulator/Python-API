import numpy as np
likelihood = 0.02
progression_probability = 0
for i in range(40):
    progression_probability = np.random.binomial(100, likelihood)
    likelihood += 0.02
print(progression_probability)
