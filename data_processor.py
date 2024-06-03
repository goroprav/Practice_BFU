import numpy as np

class DataProcessor:
    def __init__(self, data_x, data_y=None, coefficient_1=0, coefficient_2=0, lambda_0=None, temp_T=None):
        self.data_x = np.array(data_x, dtype=float)
        self.data_y = np.array(data_y, dtype=float) if data_y is not None else None
        self.coefficient_1 = coefficient_1
        self.coefficient_2 = coefficient_2
        self.lambda_0 = lambda_0
        self.temp_T = temp_T

    def process_x1(self):
        processed_data_x = self.data_x * (self.data_x * self.coefficient_1 + self.coefficient_2)
        return processed_data_x

    def process_x2_y2(self):
        if self.data_y is None or self.lambda_0 is None or self.temp_T is None:
            raise ValueError("data_y, lambda_0, and temp_T must be provided for processing X2 and Y2")

        c = 299792458
        pi = np.pi
        h = 6.626069573 * 10**(-34)
        k = 1.380649 * 10**(-23)
        v_0 = c / self.lambda_0

        new_x = self.data_x * (self.data_x * self.coefficient_1 + self.coefficient_2)
        v_j = (new_x * c) / (2 * pi)
        exp_term = np.exp((-h * c * v_j) / (k * self.temp_T))
        
        new_y = ((2**4) * (pi**4) / 45 * ((v_0 - v_j)**4 / (1 - exp_term))
                 * h / (8 * (pi**4) * c * v_j) * self.data_y * 10**(-6))
        
        return new_x, new_y
