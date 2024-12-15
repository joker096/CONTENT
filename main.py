# pip install python-dotenv
# pip install botasaurus
from botasaurus.browser import browser, Driver, Wait
import os
import time
from dotenv import load_dotenv
import pyperclip
import requests
from io import BytesIO
from PIL import Image

# Глобальный счетчик для изображений
global_image_counter = 0
# Количество изображений для скачивания
num_images_to_download = 4  # Например, загрузить 4 изображения из каждого запроса
# guidance scale
guidance='4.9'
# fixed seed
seed='92258244404'
# negative prompt
negative_prompt = 'NSFW, watermark'

# Загрузка переменных из .env
load_dotenv()
login = os.getenv("LOGIN")
password = os.getenv("PASSWORD")

# Папка для файлов
base_dir = os.path.dirname(__file__)
images_dir = os.path.join(base_dir, 'images')

# Создаем папки, если они не существуют
os.makedirs(images_dir, exist_ok=True)

# URL для входа и получения данных
login_url = 'https://piclumen.com/app/account'
dashboard_url = 'https://piclumen.com/app/image-generator/create'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
}

# Логин и пароль
login_data = {
    'email': os.getenv("LOGIN"),
    'password': os.getenv("PASSWORD")
}

# Чтение запросов из текстового файла
def read_queries_from_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print(f"Файл {file_path} не найден.")
        return []

def process_image_links(driver, images_dir):
    """Обрабатывает ссылки на изображения и загружает их."""
    img_elements = driver.get_all_image_links() # list of all images at page
    print(img_elements)
    normal_urls = [url for url in img_elements if "/normal/" in url]
    # Ограничиваем количество скачиваемых изображений
    return normal_urls

@browser(
    # add_arguments=['--headless=new'],
    wait_for_complete_page_load=False,
    reuse_driver=True
)
def piclumen(driver: Driver, data):
    global global_image_counter  # Используем глобальный счетчик
    try:
        driver.get(login_url, wait=5)
        driver.type('input[placeholder="Email"]', login, wait=1)
        driver.type('input[placeholder="Password"]', password, wait=1)
        driver.click('#app > div > div.content.overflow-x-hidden.dark > div.absolute.pb-16.top-0.left-0.w-screen.min-h-full.h-max.flex.justify-center.items-center.text-white > div.w-full.md\:w-\[488px\].relative.z-10.bg-black\/50.opacity-90.backdrop-blur-3xl.mb-24.md\:mb-0.md\:rounded-3xl.overflow-hidden > div > div.w-80.mx-auto.sign-in-account > div > div.mt-8.w-full > button', wait=5)
        driver.get(dashboard_url, wait=10)

        # settings
        driver.click('#app > div > div.flex.h-screen.box-border.dark\:bg-black.bg-zinc-200.max-md\:flex-wrap-reverse > div.w-full.relative > div > div.h-screen.relative.scroll-box.overflow-y-auto.flex > div.shrink-0.h-full > div > div > div.tool-bar-item', wait=3)
        
        # Считываем запросы из файла
        queries = read_queries_from_file(os.path.join(base_dir, 'queries.txt'))  # путь к вашему файлу с запросами
        
        for query in queries:
            if not query:
                continue
            print(f"Обрабатываем запрос: {query}")            
            if query:  # Проверяем, что запрос не пустой
                try:
                    # 4 images per iteration
                    driver.click('#confExtendArea > div > div.flex.gap-4.shrink-0.ml-2 > div:nth-child(3) > div > div:nth-child(4)', wait=3)  

                    # # settings input
                    # driver.type('#app > div > div.flex.h-screen.box-border.dark\:bg-black.bg-zinc-200.max-md\:flex-wrap-reverse > div.w-full.relative > div > div.h-screen.relative.scroll-box.overflow-y-auto.flex > div.shrink-0.h-full > div > div.border-r.p-4.border-solid.dark\:border-dark-bg-2.w-\[336px\] > div > div:nth-child(1) > div.mt-1.rounded-lg.relative.dark\:bg-dark-bg-2.bg-white.w-full.pb-2 > div > div > div.n-input__textarea.n-scrollbar > textarea', negative_prompt, wait=1)
                    # if guidance is not None:
                    #     driver.type('#app > div > div.flex.h-screen.box-border.dark\:bg-black.bg-zinc-200.max-md\:flex-wrap-reverse > div.w-full.relative > div > div.h-screen.relative.scroll-box.overflow-y-auto.flex > div.shrink-0.h-full > div > div.border-r.p-4.border-solid.dark\:border-dark-bg-2.w-\[336px\] > div > div:nth-child(2) > div.mt-1.flex.items-center.gap-2 > div.n-input-number.w-32.rounded-lg.shrink-0.text-center.dark\:bg-dark-bg-2.bg-white.input-number-h-32 > div > div.n-input-wrapper > div.n-input__input > input', guidance, wait=1)
                    # if seed is not None:
                    #     driver.click('#app > div > div.flex.h-screen.box-border.dark\:bg-black.bg-zinc-200.max-md\:flex-wrap-reverse > div.w-full.relative > div > div.h-screen.relative.scroll-box.overflow-y-auto.flex > div.shrink-0.h-full > div > div.border-r.p-4.border-solid.dark\:border-dark-bg-2.w-\[336px\] > div > div:nth-child(4) > div > div.mt-1.flex.items-center.gap-2 > div.seed-group > div:nth-child(2) > span', wait=1)
                    #     driver.type('#app > div > div.flex.h-screen.box-border.dark\:bg-black.bg-zinc-200.max-md\:flex-wrap-reverse > div.w-full.relative > div > div.h-screen.relative.scroll-box.overflow-y-auto.flex > div.shrink-0.h-full > div > div.border-r.p-4.border-solid.dark\:border-dark-bg-2.w-\[336px\] > div > div:nth-child(4) > div > div.mt-1.flex.items-center.gap-2 > div.w-32.rounded-lg.dark\:bg-dark-bg-2.bg-white.border-solid.border-red-500.border > input', seed, wait=1)

                    # Запрос на генерацию изображения
                    driver.type('textarea', query, wait=2)          

                    # Клик на Generate
                    driver.click(f'#confExtendArea > div > div.mt-3.flex.items-center.gap-2\.5.shrink-0 > div > div.flex.gap-3 > button > span', wait=3)
                    time.sleep(80)                    

                    normal_urls = process_image_links(driver, images_dir) 

                    # Скачивание и сохранение изображений
                    for url in normal_urls[:num_images_to_download]:  # Ограничиваем количество изображений
                        try:
                            # Скачиваем изображение
                            response = requests.get(url)
                            response.raise_for_status()  # Проверка на ошибки

                            # Открываем изображение
                            img = Image.open(BytesIO(response.content))

                             # Используем глобальный счетчик для имени файла
                            global_image_counter += 1

                            # Преобразуем в PNG и сохраняем
                            output_path = os.path.join(images_dir, f"image_{global_image_counter}.png")
                            img.save(output_path, 'PNG')
                            print(f"Сохранено изображение: {output_path}")
                        except Exception as e:
                            print(f"Не удалось сохранить изображение по URL {url}: {e}")               
                                   
                except Exception as e:
                    print(f"Ошибка при обработке запроса '{query}': {e}")
                    continue  # Переходим к следующему запросу, если произошла ошибка

    except Exception as e:
        print(f"Ошибка на странице: {e}")

# Запускаем браузер
piclumen()
