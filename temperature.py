import numpy as np

class TemperatureEvolution:
    def __init__(self) -> None:
        pass

    def cooling_law(self, T_hot, T_cold, k, t):
        return T_cold + (T_hot - T_cold)*np.exp(-k*t)