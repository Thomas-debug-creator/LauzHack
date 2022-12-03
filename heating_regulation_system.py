import matplotlib.pyplot as plt
import numpy as np

class HeatingRegulationSystem:

    def __init__(self, T_min, T_ideal) -> None: 
        self.T_min = T_min
        self.T_ideal = T_ideal
        # self.heat_regulation_curve = 