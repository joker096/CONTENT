import os
import shutil
from sklearn.model_selection import train_test_split

# Путь к исходным данным
images_dir = r'f:\PYTHON\BOTS\RollercoinBot-master\RollerCoin.v11i.yolov11\images'
labels_dir = r'f:\PYTHON\BOTS\RollercoinBot-master\RollerCoin.v11i.yolov11\labels'

# Папки для train и val
train_images_dir = r'f:\PYTHON\BOTS\RollercoinBot-master\RollerCoin.v11i.yolov11\train\images'
train_labels_dir = r'f:\PYTHON\BOTS\RollercoinBot-master\RollerCoin.v11i.yolov11\train\labels'
val_images_dir = r'f:\PYTHON\BOTS\RollercoinBot-master\RollerCoin.v11i.yolov11\val\images'
val_labels_dir = r'f:\PYTHON\BOTS\RollercoinBot-master\RollerCoin.v11i.yolov11\val\labels'

# Создание папок, если они не существуют
os.makedirs(train_images_dir, exist_ok=True)
os.makedirs(train_labels_dir, exist_ok=True)
os.makedirs(val_images_dir, exist_ok=True)
os.makedirs(val_labels_dir, exist_ok=True)

# Разделение данных
images = [f for f in os.listdir(images_dir) if f.endswith(('.png', '.jpg', '.jpeg'))]
train_images, val_images = train_test_split(images, test_size=0.2, random_state=42)

# Копирование тренировочных данных
missing_labels = []
for img in train_images:
    img_path = os.path.join(images_dir, img)
    label_path = os.path.join(labels_dir, img.replace('.png', '.txt')
                              .replace('.jpg', '.txt')
                              .replace('.jpeg', '.txt'))

    if os.path.exists(label_path):  # Проверка на существование метки
        shutil.copy(img_path, train_images_dir)
        shutil.copy(label_path, train_labels_dir)
    else:
        missing_labels.append(img)

# Копирование валидационных данных
for img in val_images:
    img_path = os.path.join(images_dir, img)
    label_path = os.path.join(labels_dir, img.replace('.png', '.txt')
                              .replace('.jpg', '.txt')
                              .replace('.jpeg', '.txt'))

    if os.path.exists(label_path):  # Проверка на существование метки
        shutil.copy(img_path, val_images_dir)
        shutil.copy(label_path, val_labels_dir)
    else:
        missing_labels.append(img)

# Логирование пропущенных файлов
if missing_labels:
    print(f"Всего пропущено файлов: {len(missing_labels)}")
    with open("missing_labels.log", "w") as log_file:
        log_file.writelines([f"{img}\n" for img in missing_labels])
    print("Список пропущенных файлов сохранен в 'missing_labels.log'.")
else:
    print("Все данные успешно обработаны.")
