import cv2
from ultralytics import YOLO
import matplotlib.pyplot as plt
from PIL import Image

# Путь к вашей модели
model_path = r'F:\PYTHON\BOTS\RollercoinBot-master\RollerCoin.v11i.yolov11\cryptonoid.pt'

# Путь к изображению
image_path = r'F:\PYTHON\BOTS\RollercoinBot-master\RollerCoin.v11i.yolov11\images\frame_00340.png'

# Загрузка модели
model = YOLO(model_path)

# Выполнение предсказания
results = model(image_path)

# Получение предсказаний
predictions = results[0].boxes.xyxy.cpu().numpy()  # Координаты (xmin, ymin, xmax, ymax)
classes = results[0].boxes.cls.cpu().numpy()      # Классы
confidences = results[0].boxes.conf.cpu().numpy()  # Уверенность

# Открываем изображение
image = cv2.imread(image_path)

# Рисуем предсказания на изображении
for i, box in enumerate(predictions):
    xmin, ymin, xmax, ymax = map(int, box)
    class_id = int(classes[i])
    confidence = confidences[i]
    
    # Рисуем прямоугольник
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
    
    # Добавляем текст
    label = f"Class {class_id}: {confidence:.2%}"
    cv2.putText(image, label, (xmin, ymin - 10), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Сохранение изображения
output_path = r'F:\PYTHON\BOTS\RollercoinBot-master\botcoinclick\output.png'
cv2.imwrite(output_path, image)

# Просмотр через PIL
Image.open(output_path).show()

# Отображение через Matplotlib
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
plt.imshow(image_rgb)
plt.axis('off')
plt.show()
