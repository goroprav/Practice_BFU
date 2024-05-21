class DataLoader:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_data(self):
        with open(self.file_path, 'r') as file:
            lines = file.readlines()
            relevant_lines = lines[8:]  # Получить строки, начиная с восьмой строки и до конца файла

        X1_columns = []
        Y1_columns = []
        X2_columns = []
        Y2_columns = []

        # Считывание X1_columns
        for line in relevant_lines:
            columns = line.split()  # Разделить строку на столбцы по пробелам
            if len(columns) >= 2:  # Проверить, что второй столбец существует
                X1_column = columns[1]  # Получить второй столбец
                if "Plot" in X1_column:  # Проверить, есть ли "Plot" во втором столбце
                    break  # Если есть "Plot", прекратить чтение
                X1_columns.append(X1_column)

        # Считывание Y1_columns
        for line in relevant_lines:
            columns = line.split()  # Разделить строку на столбцы по пробелам
            if len(columns) >= 3:  # Проверить, что третий столбец существует
                Y1_column = columns[2]  # Получить третий столбец
                if "Curve" in Y1_column:  # Проверить, есть ли "Curve" в третьем столбце
                    break  # Если есть "Curve", прекратить чтение
                Y1_columns.append(Y1_column)

        # Считывание X2_columns
        start_writing = False  # Флаг, чтобы определить, когда начинать записывать данные
        skip_next_line = False  # Флаг, чтобы пропустить следующую строку

        for line in relevant_lines:
            if "# Plot Curve (Harmonic)" in line:  # Проверить, содержит ли строка "# Plot Curve (Harmonic)"
                start_writing = True
                skip_next_line = True  # Флаг, чтобы пропустить следующую строку
                continue  # Продолжить чтение следующей строки

            if skip_next_line:
                skip_next_line = False  # Сбросить флаг, чтобы пропустить только одну строку
                continue  # Продолжить чтение следующей строки

            if start_writing:
                columns = line.split()  # Разделить строку на столбцы по пробелам
                if len(columns) >= 1:  # Проверить, что первый столбец существует
                    X2_column = columns[0]  # Получить первый столбец
                    if " " in X2_column:  # Проверить, есть ли пробел в первом столбце
                        break  # Если есть пробел, прекратить чтение
                    X2_columns.append(X2_column)

        # Считывание Y2_columns
        start_writing = False  # Флаг, чтобы определить, когда начинать записывать данные
        skip_next_line = False  # Флаг, чтобы пропустить следующую строку

        for line in relevant_lines:
            if "# Plot Curve (Harmonic)" in line:  # Проверить, содержит ли строка "# Plot Curve (Harmonic)"
                start_writing = True
                skip_next_line = True  # Флаг, чтобы пропустить следующую строку
                continue  # Продолжить чтение следующей строки

            if skip_next_line:
                skip_next_line = False  # Сбросить флаг, чтобы пропустить только одну строку
                continue  # Продолжить чтение следующей строки

            if start_writing:
                columns = line.split()  # Разделить строку на столбцы по пробелам
                if len(columns) >= 2:  # Проверить, что второй столбец существует
                    Y2_column = columns[1]  # Получить второй столбец
                    if " " in Y2_column:  # Проверить, есть ли пробел во втором столбце
                        break  # Если есть пробел, прекратить чтение
                    Y2_columns.append(Y2_column)

        return X1_columns, Y1_columns, X2_columns, Y2_columns
    

