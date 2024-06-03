import math

class DataProcessor:
    def __init__(self, data_x, data_y=None, coefficient_1=0, coefficient_2=0, lambda_0=None, temp_T=None):
        self.data_x = data_x
        self.data_y = data_y
        self.coefficient_1 = coefficient_1
        self.coefficient_2 = coefficient_2
        self.lambda_0 = lambda_0
        self.temp_T = temp_T

    def process_x1(self):
        processed_data_x = []
        for x in self.data_x:
            try:
                x = float(x)
                new_x = x * (x * self.coefficient_1 + self.coefficient_2)
                processed_data_x.append(new_x)
            except ValueError:
                continue
        return processed_data_x

    def process_x2_y2(self):
        if self.data_y is None or self.lambda_0 is None or self.temp_T is None:
            raise ValueError("data_y, lambda_0, and temp_T must be provided for processing X2 and Y2")

        processed_data_x = []
        processed_data_y = []
        c = 299792458
        pi = 3.14159265358979
        h = 6.626069573 * 10**(-34)
        k = 1.380649 * 10**(-23)
        v_0 = c / self.lambda_0

        for x, y in zip(self.data_x, self.data_y):
            try:
                x = float(x)
                y = float(y)
                new_x = x * (x * self.coefficient_1 + self.coefficient_2)
                v_j = (new_x * c) / (2 * pi)
                new_y = ((2**4) * (pi**4) / 45 * ((v_0 - v_j)**4 / (1 - math.exp((-h * c * v_j) / (k * self.temp_T)))) 
                         * h / (8 * (pi**4) * c * v_j) * y*10**(-6))
                processed_data_x.append(new_x)
                processed_data_y.append(new_y)
            except ValueError:
                continue
        return processed_data_x, processed_data_y
