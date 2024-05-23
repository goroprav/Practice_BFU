import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import pandas as pd
from data_loader import DataLoader
from data_processor import DataProcessor

class DataApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Обработчик")
        self.root.geometry("800x600")
        self.root.configure(bg='#2f2f2f')  # Темно-серый фон

        style = ttk.Style()
        style.configure('TButton', 
                        background='white', 
                        foreground='black', 
                        borderwidth=1, 
                        relief="solid")
        style.configure('TEntry', 
                        fieldbackground='black', 
                        foreground='white', 
                        borderwidth=1, 
                        relief="solid")
        style.configure('TLabel', 
                        background='#2f2f2f', 
                        foreground='white')
        style.configure('TOptionMenu', 
                        background='black', 
                        foreground='black', 
                        borderwidth=1, 
                        relief="solid")

        self.data = None
        self.processed_data_x = None
        self.processed_data_y = None

        self.upload_button = ttk.Button(root, text="Загрузить файл", command=self.upload_file)
        self.upload_button.grid(row=0, column=0, columnspan=4, pady=10, padx=10)

        self.data_selection = tk.StringVar(root)
        self.data_selection.set("X1 и Y1")  # Значение по умолчанию
        self.data_menu = ttk.OptionMenu(root, self.data_selection, "X1 и Y1", "X1 и Y1", "X2 и Y2", command=self.display_selected_data)
        self.data_menu.grid(row=1, column=0, columnspan=4, pady=10, padx=10)

        self.coefficient_1_label = ttk.Label(root, text="Коэффициент 1:")
        self.coefficient_1_entry = ttk.Entry(root)

        self.coefficient_2_label = ttk.Label(root, text="Коэффициент 2:")
        self.coefficient_2_entry = ttk.Entry(root)

        self.lambda_0_label = ttk.Label(root, text="lambda_0:")
        self.lambda_0_entry = ttk.Entry(root)

        self.temp_T_label = ttk.Label(root, text="temp_T:")
        self.temp_T_entry = ttk.Entry(root)

        self.process_button = ttk.Button(root, text="Обработать данные", command=self.process_data)

        self.output_text = tk.Text(root, height=20, width=100, bg='black', fg='white', wrap='none')

        self.save_button = ttk.Button(root, text="Сохранить в Excel", command=self.save_to_excel)

        self.show_or_hide_widgets()

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
        if selected_data == "X1 и Y1":
            data_x = self.data[0]
            data_y = self.data[1]
        elif selected_data == "X2 и Y2":
            data_x = self.data[2]
            data_y = self.data[3]

        for x, y in zip(data_x, data_y):
            self.output_text.insert(tk.END, f"{x}\t\t{y}\n")

        self.show_or_hide_widgets()

    def show_or_hide_widgets(self):
        if self.data_selection.get() == "X1 и Y1":
            self.coefficient_1_label.grid(row=2, column=0, pady=10, padx=10, sticky='e')
            self.coefficient_1_entry.grid(row=2, column=1, pady=10, padx=10, sticky='w')
            self.coefficient_2_label.grid(row=3, column=0, pady=10, padx=10, sticky='e')
            self.coefficient_2_entry.grid(row=3, column=1, pady=10, padx=10, sticky='w')
            self.lambda_0_label.grid_remove()
            self.lambda_0_entry.grid_remove()
            self.temp_T_label.grid_remove()
            self.temp_T_entry.grid_remove()
            self.process_button.grid(row=4, column=0, columnspan=4, pady=10, padx=10)
            self.output_text.grid(row=5, column=0, columnspan=4, pady=10, padx=10)
            self.save_button.grid(row=6, column=0, columnspan=4, pady=10, padx=10)
        else:
            self.coefficient_1_label.grid(row=2, column=0, pady=10, padx=10, sticky='e')
            self.coefficient_1_entry.grid(row=2, column=1, pady=10, padx=10, sticky='w')
            self.coefficient_2_label.grid(row=3, column=0, pady=10, padx=10, sticky='e')
            self.coefficient_2_entry.grid(row=3, column=1, pady=10, padx=10, sticky='w')
            self.lambda_0_label.grid(row=2, column=2, pady=10, padx=10, sticky='e')
            self.lambda_0_entry.grid(row=2, column=3, pady=10, padx=10, sticky='w')
            self.temp_T_label.grid(row=3, column=2, pady=10, padx=10, sticky='e')
            self.temp_T_entry.grid(row=3, column=3, pady=10, padx=10, sticky='w')
            self.process_button.grid(row=4, column=0, columnspan=4, pady=10, padx=10)
            self.output_text.grid(row=5, column=0, columnspan=4, pady=10, padx=10)
            self.save_button.grid(row=6, column=0, columnspan=4, pady=10, padx=10)

    def process_data(self):
        if not self.data:
            messagebox.showerror("Ошибка", "Сначала загрузите файл")
            return

        selected_data = self.data_selection.get()
        if selected_data == "X1 и Y1":
            data_x = self.data[0]
            data_y = self.data[1]
        elif selected_data == "X2 и Y2":
            data_x = self.data[2]
            data_y = self.data[3]

        try:
            coefficient_1 = float(self.coefficient_1_entry.get())
            coefficient_2 = float(self.coefficient_2_entry.get())
            lambda_0 = float(self.lambda_0_entry.get())*10**(-9)
            temp_T = float(self.temp_T_entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные значения для коэффициентов")
            return

        processor = DataProcessor(data_x, data_y, coefficient_1, coefficient_2, lambda_0, temp_T)
        self.processed_data_x, self.processed_data_y = processor.process_data()

        self.output_text.delete('1.0', tk.END)
        for x, y, new_x, new_y in zip(data_x, data_y, self.processed_data_x, self.processed_data_y):
            self.output_text.insert(tk.END, f"{x}\t\t{y}\t\t{new_x}\t\t{new_y}\n")

    def save_to_excel(self):
        if not self.processed_data_x or not self.processed_data_y:
            messagebox.showerror("Ошибка", "Сначала обработайте данные")
            return

        selected_data = self.data_selection.get()
        if selected_data == "X1 и Y1":
            original_data_x = self.data[0]
            original_data_y = self.data[1]
        elif selected_data == "X2 и Y2":
            original_data_x = self.data[2]
            original_data_y = self.data[3]

        df = pd.DataFrame({
            'Original X': original_data_x,
            'Original Y': original_data_y,
            'Processed X': self.processed_data_x,
            'Processed Y': self.processed_data_y
        })

        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False)
            messagebox.showinfo("Сохранение файла", "Файл успешно сохранен")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataApp(root)
    root.mainloop()
