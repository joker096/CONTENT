from mtranslate import translate
import os
import re
from tqdm import tqdm  # Для индикатора прогресса

# Пути к файлам
base_dir = os.path.dirname(__file__)
input_file = os.path.join(base_dir, 'input.txt')
output_file = os.path.join(base_dir, 'output.txt')

# Функция для перевода текста
def translate_text(text, target_lang='en', source_lang='auto'):
    try:
        return translate(text, target_lang, source_lang)
    except Exception as e:
        print(f"Ошибка при переводе строки: {text}\n{e}")
        return text  # Возвращаем оригинальный текст в случае ошибки

# Проверка наличия букв в строке
def contains_letters(text):
    return bool(re.search(r'[a-zA-Zа-яА-Я]', text))

# Исходный и целевой языки
source_lang = 'auto'  # Автоматическое определение исходного языка
target_lang = 'en'    # Язык перевода

# Чтение файла, перевод строк и запись результата
try:
    # Считываем все строки заранее для определения общего количества
    with open(input_file, "r", encoding="utf-8") as infile:
        lines = infile.readlines()

    with open(output_file, "w", encoding="utf-8") as outfile:
        # Используем tqdm для отображения прогресса
        for line in tqdm(lines, desc="Перевод строк", unit="строка"):
            line = line.strip()  # Удаление лишних пробелов и символов новой строки
            if line:  # Пропустить пустые строки
                if contains_letters(line):
                    # Переводим только строки с буквами
                    translated_line = translate_text(line, target_lang, source_lang)
                    outfile.write(translated_line + "\n")
                else:
                    # Просто записываем строки без букв
                    outfile.write(line + "\n")
    print(f"\nПеревод завершен! Результаты сохранены в файл: {output_file}")
except FileNotFoundError:
    print(f"Файл {input_file} не найден. Проверьте путь и название файла.")
except Exception as e:
    print(f"Произошла ошибка: {e}")
