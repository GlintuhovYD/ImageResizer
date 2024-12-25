import tkinter as tk
from tkinter import filedialog

import image_processing
import ui_utils

def update_fields():
    if task_var.get() == "crop":
        width_label.grid(row=7, column=0, sticky="w")
        width_entry.grid(row=7, column=1, sticky="e")
        height_label.grid(row=8, column=0, sticky="w")
        height_entry.grid(row=8, column=1, sticky="e")
        max_width_label.grid_forget()
        max_width_entry.grid_forget()
    elif task_var.get() == "resize":
        width_label.grid_forget()
        width_entry.grid_forget()
        height_label.grid_forget()
        height_entry.grid_forget()
        max_width_label.grid(row=7, column=0, sticky="w")
        max_width_entry.grid(row=7, column=1, sticky="e")

def browse_input_folder():
    folder_path = filedialog.askdirectory()
    input_folder_path_entry.delete(0, tk.END)
    input_folder_path_entry.insert(0, folder_path)


def browse_output_folder():
    folder_path = filedialog.askdirectory()
    output_folder_path_entry.delete(0, tk.END)
    output_folder_path_entry.insert(0, folder_path)


def process_images():
    input_folder_path = input_folder_path_entry.get()
    output_folder_path = output_folder_path_entry.get()

    if not input_folder_path or not output_folder_path:
        ui_utils.show_error("Выберите папки ввода и вывода!")
        return

    naming_method = naming_method_var.get()
    task = task_var.get()
    output_ext = ext_var.get().lower()

    try:
        if task == "crop":
            width = int(width_entry.get())
            height = int(height_entry.get())
            if width <= 0 or height <= 0:
                ui_utils.show_error("Ширина и высота должны быть больше нуля!")
                return
            if image_processing.process_images_crop(input_folder_path, output_folder_path, width, height, output_ext,
                                                    naming_method):
                ui_utils.show_success("Обрезка завершена успешно!")
            else:
                ui_utils.show_error("Ошибка при обрезке изображений!")

        elif task == "resize":
            max_width = int(max_width_entry.get())
            if max_width <= 0:
                ui_utils.show_error("Максимальная ширина должна быть больше нуля!")
                return
            if image_processing.process_images_resize(input_folder_path, output_folder_path, max_width, output_ext,
                                                    naming_method):
                ui_utils.show_success("Изменение размера завершено успешно!")
            else:
                ui_utils.show_error("Ошибка при изменении размера изображений!")
        else:
            ui_utils.show_error("Выберите задачу!")
    except ValueError:
        ui_utils.show_error("Неверные числовые значения!")
    except Exception as e:
        ui_utils.show_error(f"Произошла непредвиденная ошибка: {e}")


root = tk.Tk()
root.title("Обработка изображений")
root.resizable(False, False)

input_folder_path_label = tk.Label(root, text="Путь к папке ввода:")
input_folder_path_label.grid(row=0, column=0, sticky="w")

input_folder_path_entry = tk.Entry(root, width=50)
input_folder_path_entry.grid(row=0, column=1, sticky="e")

browse_input_button = tk.Button(root, text="Обзор...", command=browse_input_folder)
browse_input_button.grid(row=0, column=2)

output_folder_path_label = tk.Label(root, text="Путь к папке вывода:")
output_folder_path_label.grid(row=1, column=0, sticky="w")

output_folder_path_entry = tk.Entry(root, width=50)
output_folder_path_entry.grid(row=1, column=1, sticky="e")

browse_output_button = tk.Button(root, text="Обзор...", command=browse_output_folder)
browse_output_button.grid(row=1, column=2)

task_var = tk.StringVar(value="crop")
task_label = tk.Label(root, text="Задача:")
task_label.grid(row=2, column=0, sticky="w")
crop_radio = tk.Radiobutton(root, text="Обрезка", variable=task_var, value="crop")
crop_radio.grid(row=3, column=0, sticky="w")
resize_radio = tk.Radiobutton(root, text="Изменение размера", variable=task_var, value="resize")
resize_radio.grid(row=4, column=0, sticky="w")

width_label = tk.Label(root, text="Ширина:")
width_entry = tk.Entry(root, width=10)
height_label = tk.Label(root, text="Высота:")
height_entry = tk.Entry(root, width=10)
max_width_label = tk.Label(root, text="Макс. ширина:")
max_width_entry = tk.Entry(root, width=10)


naming_method_var = tk.StringVar(value="number")
naming_method_label = tk.Label(root, text="Метод именования:")
naming_method_label.grid(row=5, column=0, sticky="w")
naming_method_number_radio = tk.Radiobutton(root, text="Нумерация", variable=naming_method_var, value="number")
naming_method_number_radio.grid(row=6, column=0, sticky="w")
naming_method_original_radio = tk.Radiobutton(root, text="Оригинальное имя", variable=naming_method_var, value="original")
naming_method_original_radio.grid(row=6, column=1, sticky="w")

ext_var = tk.StringVar(value="png")
ext_label = tk.Label(root, text="Расширение:")
ext_label.grid(row=9, column=0, sticky="w")
ext_entry = tk.Entry(root, textvariable=ext_var, width=10)

ext_entry.grid(row=9, column=1, sticky="e")
ext_var.set("png")

process_button = tk.Button(root, text="Обработать", command=process_images)
process_button.grid(row=10, column=0, columnspan=3)

result_label = tk.Label(root, text="")
result_label.grid(row=11, column=0, columnspan=3)

task_var.trace("w", lambda *args: update_fields())
update_fields()

root.mainloop()
