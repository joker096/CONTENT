import cv2
import os
import shutil

# Путь к видеофайлу
video_path = r'F:\PYTHON\BOTS\RollercoinBot-master\demo\detection_video\input\cryptonoid.mp4'

# Директория для сохранения кадров
frames_dir = r'f:\PYTHON\BOTS\RollercoinBot-master\demo\detection_video\output\frames'

# Очищаем папку с кадрами, если она существует
if os.path.exists(frames_dir):
    shutil.rmtree(frames_dir)  # Удаляет папку и все её содержимое
os.makedirs(frames_dir, exist_ok=True)  # Создает пустую папку

# Загрузка видео
video_capture = cv2.VideoCapture(video_path)

# Проверка, удалось ли открыть видео
if not video_capture.isOpened():
    print("Не удалось открыть видео.")
    exit()

frame_rate = video_capture.get(cv2.CAP_PROP_FPS)  # Частота кадров видео
frame_count = 0

while True:
    # Чтение следующего кадра
    success, frame = video_capture.read()
    if not success:
        break  # Кадры закончились

    # Сохранение каждого кадра
    frame_file = os.path.join(frames_dir, f"frame_{frame_count:05d}.png")
    cv2.imwrite(frame_file, frame)
    frame_count += 1

print(f"Извлечено {frame_count} кадров. Кадры сохранены в: {frames_dir}")

# Освобождение ресурсов
video_capture.release()