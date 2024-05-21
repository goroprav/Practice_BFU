class DataProcessor:
    def __init__(self, data, coefficient_1, coefficient_2):
        self.data = data
        self.coefficient_1 = coefficient_1
        self.coefficient_2 = coefficient_2

    def process_data(self):
        processed_data = []
        for value in self.data:
            try:
                value = float(value)  # Преобразование строки в число
                new_value = value * self.coefficient_1 + self.coefficient_2
                processed_data.append(new_value)
            except ValueError:
                # Если значение не может быть преобразовано в float, пропускаем его
                continue
        return processed_data
