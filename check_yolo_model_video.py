import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt
from PIL import Image

# Путь к вашей модели
model_path = r'F:\PYTHON\BOTS\RollercoinBot-master\RollerCoin.v11i.yolov11\botcoinclick.pt'
# model_path = r'F:\PYTHON\BOTS\RollercoinBot-master\RollerCoin.v11i.yolov11\cryptonoid.pt'

# Путь к видео
video_path = r'F:\PYTHON\BOTS\RollercoinBot-master\botcoinclick\coins_video.mp4'
# video_path = r'F:\PYTHON\BOTS\RollercoinBot-master\demo\detection_video\input\cryptonoid.mp4'

# Папка для сохранения обработанных кадров
output_frames_path = r'F:\PYTHON\BOTS\RollercoinBot-master\botcoinclick\output_frames'

# Путь для сохранения выходного видео
output_video_path = r'F:\PYTHON\BOTS\RollercoinBot-master\botcoinclick\output_video.mp4'

# Загрузка модели
model = YOLO(model_path)

# Открытие видео
capture = cv2.VideoCapture(video_path)

# Получаем параметры видео
frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = int(capture.get(cv2.CAP_PROP_FPS))

# Настройка записи выходного видео
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Кодек для записи
out = cv2.VideoWriter(output_video_path, fourcc, fps, (frame_width, frame_height))

frame_id = 0
while capture.isOpened():
    ret, frame = capture.read()
    if not ret:
        break

    frame_id += 1
    print(f"Обработка кадра {frame_id}")

    # Выполнение предсказания
    results = model(frame)

    # Получение предсказаний
    predictions = results[0].boxes.xyxy.cpu().numpy()  # Координаты (xmin, ymin, xmax, ymax)
    classes = results[0].boxes.cls.cpu().numpy()      # Классы
    confidences = results[0].boxes.conf.cpu().numpy()  # Уверенность

    # Рисуем предсказания на кадре
    for i, box in enumerate(predictions):
        xmin, ymin, xmax, ymax = map(int, box)
        class_id = int(classes[i])
        confidence = confidences[i]
        
        # Рисуем прямоугольник
        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
        
        # Добавляем текст
        label = f"Class {class_id}: {confidence:.2%}"
        cv2.putText(frame, label, (xmin, ymin - 10), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # Сохраняем кадр в выходное видео
    out.write(frame)

# Освобождаем ресурсы
capture.release()
out.release()

print("Обработка видео завершена.")
