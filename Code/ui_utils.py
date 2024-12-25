import tkinter as tk

def show_error(message):
    error_window = tk.Toplevel()
    error_window.title("Ошибка")
    error_label = tk.Label(error_window, text=message)
    error_label.pack(pady=10)
    ok_button = tk.Button(error_window, text="OK", command=error_window.destroy)
    ok_button.pack(pady=10)
    error_window.transient(master=None) # this makes sure the window is on top

def show_success(message):
    success_window = tk.Toplevel()
    success_window.title("Успех")
    success_label = tk.Label(success_window, text=message)
    success_label.pack(pady=10)
    ok_button = tk.Button(success_window, text="OK", command=success_window.destroy)
    ok_button.pack(pady=10)
    success_window.transient(master=None)