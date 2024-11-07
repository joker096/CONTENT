from bs4 import BeautifulSoup
import os

# Папка для сохранения данных
base_dir = os.path.dirname(__file__)
input_file = os.path.join(base_dir, 'article.html') 
output_file = os.path.join(base_dir, 'cleaned_output.html')

def clean_html_table(html_content):
    # Парсим HTML с помощью BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Удаляем все <style> и <script> теги
    for tag in soup(['style', 'script']):
        tag.decompose()

    # Удаляем все атрибуты (например, inline-стили) у тегов
    for tag in soup.find_all(True):  # True находит все теги
        tag.attrs = {}  # Очистка всех атрибутов

    # Возвращаем очищенный HTML
    cleaned_html = soup.prettify()
    return cleaned_html

# Пример использования
if __name__ == '__main__':
    # with open(input_file, 'r', encoding='utf-8', errors='replace') as file:
    #     html_content = file.read()

    # Чтение HTML-файла с проверкой альтернативных кодировок
    try:
        with open(input_file, 'r', encoding='cp1251') as file:  # Пробуем открыть с cp1251
            html_content = file.read()
    except UnicodeDecodeError:
        with open(input_file, 'r', encoding='latin-1') as file:  # Если не получилось, пробуем latin-1
            html_content = file.read()

    # Очистка таблиц и HTML-кода
    cleaned_html = clean_html_table(html_content)

    # Сохранение результата в новый файл
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(cleaned_html)

    print("HTML успешно очищен и сохранён в 'cleaned_output.html'")

