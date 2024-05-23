import math

class DataProcessor:
    def __init__(self, data_x, data_y, coefficient_1, coefficient_2, lambda_0, temp_T):
        self.data_x = data_x
        self.data_y = data_y
        self.coefficient_1 = coefficient_1
        self.coefficient_2 = coefficient_2
        self.lambda_0 = lambda_0
        self.temp_T = temp_T

    def process_data(self):
        processed_data_x = []
        processed_data_y = []
        c=299792458
        pi=3.14159265358979
        h=6.626069573*10**(-34)
        k=1.380649*10**(-23)
        v_0=c/self.lambda_0


        for x, y in zip(self.data_x, self.data_y):
            try:
                x = float(x)
                y = float(y)
                new_x = x * (x * self.coefficient_1 + self.coefficient_2)
                v_j=(new_x*c)/(2*pi)
                new_y = ( (2**4) * (pi**4) )/45 * ((v_0 - v_j)**4/(1-math.exp((-h*c*v_j)/(k*self.temp_T)))) * h/(8* (pi**4) * c * v_j) * y
                processed_data_x.append(new_x)
                processed_data_y.append(new_y)
            except ValueError:
                continue
        return processed_data_x, processed_data_y
