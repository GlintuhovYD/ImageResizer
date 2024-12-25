import os
import pathlib

def get_next_filename(folder_path, output_ext):
    try:
        folder = pathlib.Path(folder_path)
        existing_files = [int(f.stem) for f in folder.glob(f"*.{output_ext}") if f.stem.isdigit()]
        return max(existing_files) + 1 if existing_files else 1
    except (ValueError, IndexError) as e:
        return f"Ошибка: {e}"


def save_image(image, folder_path, filename_or_index, output_ext, naming_method):
    if image is None:
        return "Ошибка: Изображение не задано"

    try:
        if naming_method == "number":
            next_num = get_next_filename(folder_path, output_ext)
            if isinstance(next_num, str):
                return next_num
            output_filename = os.path.join(folder_path, f"{next_num}.{output_ext}")
        elif naming_method == "original":
            # Здесь важно использовать оригинальное имя файла
            name, ext = os.path.splitext(filename_or_index)
            if ext.lower() != f".{output_ext.lower()}":
                output_filename = os.path.join(folder_path, f"{name}.{output_ext}")
            else:
                output_filename = os.path.join(folder_path, filename_or_index) # Используем оригинальное имя, если расширение совпадает
        else:
            return "Ошибка: Неизвестный метод именования"

        os.makedirs(folder_path, exist_ok=True)
        image.save(output_filename)
        return None
    except FileNotFoundError:
        return f"Ошибка: Папка '{folder_path}' не найдена"
    except OSError as e:
        return f"Ошибка системы при сохранении файла: {e}"
    except AttributeError as e:
        return f"Ошибка: Не удалось сохранить изображение. Возможно, некорректный формат изображения: {e}"
    except Exception as e:
        return f"Произошла непредвиденная ошибка при сохранении изображения: {e}"
