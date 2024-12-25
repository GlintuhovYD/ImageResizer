from PIL import Image
import os

import file_utils
import ui_utils

def process_images_crop(input_folder_path, output_folder_path, width, height, output_ext, naming_method):
    files = [f for f in os.listdir(input_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    if not files:
        ui_utils.show_error("Нет изображений в папке!")
        return False

    # Проверка существования папки
    if not os.path.exists(output_folder_path) or not os.path.isdir(output_folder_path):
        ui_utils.show_error(f"Папка '{output_folder_path}' не существует или недоступна.")
        return False

    for i, filename in enumerate(files):
        input_filepath = os.path.join(input_folder_path, filename)
        try:
            with Image.open(input_filepath) as img:
                cropped_img = img.crop((0, 0, min(width, img.width), min(height, img.height)))
                error_message = file_utils.save_image(cropped_img, output_folder_path, i + 1 if naming_method == "number" else filename, output_ext, naming_method)
                if error_message:
                    ui_utils.show_error(f"Ошибка при сохранении {filename}: {error_message}")
                    return False
        except Exception as e:
            ui_utils.show_error(f"Ошибка при обработке {filename}: {e}")
            return False

    return True


def process_images_resize(input_folder_path, output_folder_path, max_width, output_ext, naming_method):
    files = [f for f in os.listdir(input_folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))]
    if not files:
        ui_utils.show_error("Нет изображений в папке!")
        return False

    # Проверка существования папки
    if not os.path.exists(output_folder_path) or not os.path.isdir(output_folder_path):
        ui_utils.show_error(f"Папка '{output_folder_path}' не существует или недоступна.")
        return False

    for i, filename in enumerate(files):
        input_filepath = os.path.join(input_folder_path, filename)
        try:
            with Image.open(input_filepath) as img:
                w, h = img.size
                if w > max_width:
                    new_width = max_width
                    new_height = int(h * (max_width / w))
                    resized_img = img.resize((new_width, new_height), Image.BILINEAR)
                else:
                    resized_img = img
                error_message = file_utils.save_image(resized_img, output_folder_path, i + 1 if naming_method == "number" else filename, output_ext, naming_method)
                if error_message:
                    ui_utils.show_error(f"Ошибка при сохранении {filename}: {error_message}")
                    return False
        except Exception as e:
            ui_utils.show_error(f"Ошибка при обработке {filename}: {e}")
            return False

    return True