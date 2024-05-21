import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
from data_loader import DataLoader
from data_processor import DataProcessor

class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Приложение для обработки данных")
        self.root.geometry("800x600")

        self.data = None
        self.processed_data = None

        self.upload_button = tk.Button(root, text="Загрузить файл", command=self.upload_file)
        self.upload_button.pack()

        self.data_selection = tk.StringVar(root)
        self.data_selection.set("X1")  # Значение по умолчанию
        self.data_menu = tk.OptionMenu(root, self.data_selection, "X1", "Y1", "X2", "Y2", command=self.display_selected_data)
        self.data_menu.pack()

        self.coefficient_1_label = tk.Label(root, text="Коэффициент 1:")
        self.coefficient_1_label.pack()
        self.coefficient_1_entry = tk.Entry(root)
        self.coefficient_1_entry.pack()

        self.coefficient_2_label = tk.Label(root, text="Коэффициент 2:")
        self.coefficient_2_label.pack()
        self.coefficient_2_entry = tk.Entry(root)
        self.coefficient_2_entry.pack()

        self.process_button = tk.Button(root, text="Обработать данные", command=self.process_data)
        self.process_button.pack()

        self.output_text = tk.Text(root, height=20, width=80)
        self.output_text.pack()

        self.save_button = tk.Button(root, text="Сохранить в Excel", command=self.save_to_excel)
        self.save_button.pack()

    def upload_file(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            loader = DataLoader(file_path)
            self.data = loader.load_data()
            messagebox.showinfo("Загрузка файла", "Файл успешно загружен")

    def display_selected_data(self, selected):
        if not self.data:
            messagebox.showerror("Ошибка", "Сначала загрузите файл")
            return

        self.output_text.delete('1.0', tk.END)
        selected_data = self.data_selection.get()
        if selected_data == "X1":
            data_to_display = self.data[0]
        elif selected_data == "Y1":
            data_to_display = self.data[1]
        elif selected_data == "X2":
            data_to_display = self.data[2]
        elif selected_data == "Y2":
            data_to_display = self.data[3]

        for value in data_to_display:
            self.output_text.insert(tk.END, f"{value}\n")

    def process_data(self):
        if not self.data:
            messagebox.showerror("Ошибка", "Сначала загрузите файл")
            return

        selected_data = self.data_selection.get()
        if selected_data == "X1":
            data_to_process = self.data[0]
        elif selected_data == "Y1":
            data_to_process = self.data[1]
        elif selected_data == "X2":
            data_to_process = self.data[2]
        elif selected_data == "Y2":
            data_to_process = self.data[3]

        try:
            coefficient_1 = float(self.coefficient_1_entry.get())
            coefficient_2 = float(self.coefficient_2_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные значения для коэффициентов")
            return

        processor = DataProcessor(data_to_process, coefficient_1, coefficient_2)
        self.processed_data = processor.process_data()

        self.output_text.delete('1.0', tk.END)
        for original, new in zip(data_to_process, self.processed_data):
            self.output_text.insert(tk.END, f"{original}\t\t{new}\n")

    def save_to_excel(self):
        if not self.processed_data:
            messagebox.showerror("Ошибка", "Сначала обработайте данные")
            return

        selected_data = self.data_selection.get()
        if selected_data == "X1":
            original_data = self.data[0]
        elif selected_data == "Y1":
            original_data = self.data[1]
        elif selected_data == "X2":
            original_data = self.data[2]
        elif selected_data == "Y2":
            original_data = self.data[3]

        df = pd.DataFrame({
            'Original Data': original_data,
            'Processed Data': self.processed_data
        })

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Сохранение файла", "Файл успешно сохранен")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataApp(root)
    root.mainloop()
