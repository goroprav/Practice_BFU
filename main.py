import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QLabel, QLineEdit, QTextEdit, QFileDialog, 
                             QMessageBox, QVBoxLayout, QHBoxLayout, QWidget, QSpacerItem, QSizePolicy)
import pandas as pd
from data_loader import DataLoader
from data_processor import DataProcessor

class DataApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Обработчик")
        self.setGeometry(100, 100, 800, 600)
        
        self.setStyleSheet("background-color: lightblue;")  # Задний фон светло-голубого цвета

        self.data = None
        self.processed_data_x = None
        self.processed_data_y = None

        main_layout = QHBoxLayout()
        input_layout = QVBoxLayout()
        output_layout = QVBoxLayout()

        self.upload_button = QPushButton("Загрузить файл", self)
        self.upload_button.clicked.connect(self.upload_file)
        self.upload_button.setStyleSheet(self.get_button_style())
        input_layout.addWidget(self.upload_button)

        self.button_x1_y1 = QPushButton("X1 и Y1", self)
        self.button_x1_y1.clicked.connect(lambda: self.select_data_set("X1 и Y1"))
        self.button_x1_y1.setCheckable(True)
        self.button_x1_y1.setStyleSheet(self.get_toggle_button_style())
        input_layout.addWidget(self.button_x1_y1)

        self.button_x2_y2 = QPushButton("X2 и Y2", self)
        self.button_x2_y2.clicked.connect(lambda: self.select_data_set("X2 и Y2"))
        self.button_x2_y2.setCheckable(True)
        self.button_x2_y2.setStyleSheet(self.get_toggle_button_style())
        input_layout.addWidget(self.button_x2_y2)

        self.coefficient_1_label = QLabel("Коэффициент 1:", self)
        input_layout.addWidget(self.coefficient_1_label)
        self.coefficient_1_entry = QLineEdit(self)
        self.coefficient_1_entry.setStyleSheet(self.get_line_edit_style())
        input_layout.addWidget(self.coefficient_1_entry)

        self.coefficient_2_label = QLabel("Коэффициент 2:", self)
        input_layout.addWidget(self.coefficient_2_label)
        self.coefficient_2_entry = QLineEdit(self)
        self.coefficient_2_entry.setStyleSheet(self.get_line_edit_style())
        input_layout.addWidget(self.coefficient_2_entry)

        self.lambda_0_label = QLabel("lambda_0:", self)
        self.lambda_0_entry = QLineEdit(self)
        self.lambda_0_entry.setStyleSheet(self.get_line_edit_style())
        self.temp_T_label = QLabel("temp_T:", self)
        self.temp_T_entry = QLineEdit(self)
        self.temp_T_entry.setStyleSheet(self.get_line_edit_style())

        input_layout.addWidget(self.lambda_0_label)
        input_layout.addWidget(self.lambda_0_entry)
        input_layout.addWidget(self.temp_T_label)
        input_layout.addWidget(self.temp_T_entry)

        self.lambda_0_label.hide()
        self.lambda_0_entry.hide()
        self.temp_T_label.hide()
        self.temp_T_entry.hide()

        # Add a spacer to push the elements to the top
        spacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)
        input_layout.addItem(spacer)

        self.process_button = QPushButton("Обработать данные", self)
        self.process_button.clicked.connect(self.process_data)
        self.process_button.setStyleSheet(self.get_button_style())
        output_layout.addWidget(self.process_button)

        self.output_text = QTextEdit(self)
        self.output_text.setStyleSheet(self.get_output_text_style())
        output_layout.addWidget(self.output_text)

        self.save_button = QPushButton("Сохранить в Excel", self)
        self.save_button.clicked.connect(self.save_to_excel)
        self.save_button.setStyleSheet(self.get_button_style())
        output_layout.addWidget(self.save_button)

        main_layout.addLayout(input_layout, 1)  # Левая часть занимает 25% ширины
        main_layout.addLayout(output_layout, 3)  # Правая часть занимает 75% ширины

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def upload_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Загрузить файл", "", "All Files (*)")
        if file_path:
            loader = DataLoader(file_path)
            self.data = loader.load_data()
            QMessageBox.information(self, "Загрузка файла", "Файл успешно загружен")

    def select_data_set(self, selected):
        if not self.data:
            QMessageBox.critical(self, "Ошибка", "Сначала загрузите файл")
            return

        self.button_x1_y1.setChecked(selected == "X1 и Y1")
        self.button_x2_y2.setChecked(selected == "X2 и Y2")

        self.output_text.clear()
        if selected == "X1 и Y1":
            self.button_x1_y1.setStyleSheet(self.get_active_toggle_button_style())
            self.button_x2_y2.setStyleSheet(self.get_toggle_button_style())
            data_x = self.data[0]
            for x in data_x:
                self.output_text.append(f"{x}")

            self.lambda_0_label.hide()
            self.lambda_0_entry.hide()
            self.temp_T_label.hide()
            self.temp_T_entry.hide()
        else:
            self.button_x2_y2.setStyleSheet(self.get_active_toggle_button_style())
            self.button_x1_y1.setStyleSheet(self.get_toggle_button_style())
            data_x = self.data[2]
            data_y = self.data[3]
            for x, y in zip(data_x, data_y):
                self.output_text.append(f"{x}\t\t{y}")

            self.lambda_0_label.show()
            self.lambda_0_entry.show()
            self.temp_T_label.show()
            self.temp_T_entry.show()

    def process_data(self):
        if not self.data:
            QMessageBox.critical(self, "Ошибка", "Сначала загрузите файл")
            return

        self.output_text.clear()  # Clear old data before processing new data

        selected_data = "X1 и Y1" if self.button_x1_y1.isChecked() else "X2 и Y2"
        try:
            coefficient_1 = float(self.coefficient_1_entry.text())
            coefficient_2 = float(self.coefficient_2_entry.text())
            if selected_data == "X1 и Y1":
                data_x = self.data[0]
                processor = DataProcessor(data_x, coefficient_1=coefficient_1, coefficient_2=coefficient_2)
                self.processed_data_x = processor.process_x1()
                self.processed_data_y = None
            else:
                data_x = self.data[2]
                data_y = self.data[3]
                lambda_0 = float(self.lambda_0_entry.text()) * 10 ** (-9)
                temp_T = float(self.temp_T_entry.text())
                processor = DataProcessor(data_x, data_y, coefficient_1, coefficient_2, lambda_0, temp_T)
                self.processed_data_x, self.processed_data_y = processor.process_x2_y2()
        except ValueError:
            QMessageBox.critical(self, "Ошибка", "Введите корректные значения для коэффициентов")
            return

        self.output_text.clear()
        if selected_data == "X1 и Y1":
            for x, new_x in zip(data_x, self.processed_data_x):
                self.output_text.append(f"{x}\t\t{new_x}")
        else:
            for x, y, new_x, new_y in zip(data_x, data_y, self.processed_data_x, self.processed_data_y):
                self.output_text.append(f"{x}\t\t{y}\t\t{new_x}\t\t{new_y}")

    def save_to_excel(self):
        if not self.processed_data_x:
            QMessageBox.critical(self, "Ошибка", "Сначала обработайте данные")
            return

        selected_data = "X1 и Y1" if self.button_x1_y1.isChecked() else "X2 и Y2"
        if selected_data == "X1 и Y1":
            original_data_x = self.data[0]
            df = pd.DataFrame({
                'Original X': original_data_x,
                'Processed X': self.processed_data_x
            })
        else:
            original_data_x = self.data[2]
            original_data_y = self.data[3]
            df = pd.DataFrame({
                'Original X': original_data_x,
                'Original Y': original_data_y,
                'Processed X': self.processed_data_x,
                'Processed Y': self.processed_data_y
            })

        file_path, _ = QFileDialog.getSaveFileName(self, "Сохранить в Excel", "", "Excel files (*.xlsx)")
        if file_path:
            df.to_excel(file_path, index=False)
            QMessageBox.information(self, "Сохранение файла", "Файл успешно сохранен")

    def get_button_style(self):
        return """
        QPushButton {
            background-color: blue;
            color: white;
            border-radius: 10px;
            padding: 15px;
            font-size: 16px;
        }
        QPushButton:hover {
            background-color: darkblue;
        }
        """

    def get_toggle_button_style(self):
        return """
        QPushButton {
            background-color: lightgray;
            color: black;
            border-radius: 10px;
            padding: 15px;
            font-size: 16px;
        }
        QPushButton:checked {
            background-color: blue;
            color: white;
            border-radius: 10px;
        }
        """

    def get_active_toggle_button_style(self):
        return """
        QPushButton {
            background-color: blue;
            color: blue;
            border-radius: 10px;
        }
        QPushButton:hover {
            background-color: darkblue;
            border-radius: 10px;
        }
        """

    def get_line_edit_style(self):
        return """
        QLineEdit {
            background-color: white;
            border: 2px solid blue;
            border-radius: 10px;
            color: black;
            padding: 5px;
            outline: none;  /* Убираем обводку */
        }
        QLineEdit:focus {
            border: 2px solid darkblue;
            outline: none;  /* Убираем обводку */
        }
        """

    def get_output_text_style(self):
        return """
        QTextEdit {
            background-color: white;
            border: 2px solid blue;
            border-radius: 10px;
            color: black;
            padding: 10px;
            font-size: 12px;  /* Уменьшенный размер текста */
        }
        QTextEdit QScrollBar:vertical {
            background-color: blue;
            width: 14px;
            border-radius: 7px;
        }
        QTextEdit QScrollBar::handle:vertical {
            background-color: lightblue;
            min-height: 20px;
            border-radius: 7px;
        }
        QTextEdit QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            background: none;
            border-radius: 7px;
        }
        """

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DataApp()
    window.show()
    sys.exit(app.exec_())
