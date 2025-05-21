import cv2
import numpy as np

class CircleTracker:
    def __init__(self, camera_index=0, target_square_size=200):
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            raise IOError(f"Не удалось открыть камеру с индексом {camera_index}")

        self.target_square_size = target_square_size
        
        # Параметры HoughCircles
        self.hough_params = {
            'dp': 1.5,    
                           
            'minDist': 50,  
                           
            'param1': 50,   
                            
            'param2': 25,   
                            
            'minRadius': 20,
            'maxRadius': 300 
        }

    #Функция предобработки кадра для более точного обнаружения объекта
    def _preprocess_frame(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (9, 9), 0) 
        return blurred
    
    #Поиск круга
    def _find_circles(self, processed_frame):
        circles = cv2.HoughCircles(processed_frame, cv2.HOUGH_GRADIENT, **self.hough_params)
        if circles is not None:
            return np.uint16(np.around(circles))[0, :]
        return None
    
    # Функция отрисовки доп элементов кадра 
    def _draw_overlays(self, frame, circle_info, target_area_coords):
        x1, y1, x2, y2 = target_area_coords
        center_in_target = False

        # Центральный квадрат
        square_color = (255, 0, 0) 
        
        if circle_info is not None:
            x, y, r = circle_info
            # Рисуем круг и его центр
            cv2.circle(frame, (x, y), r, (0, 255, 0), 2)  
            cv2.circle(frame, (x, y), 2, (0, 0, 255), 3)  

            # Проверяем, попал ли центр круга в целевой квадрат
            center_in_target = (x1 <= x <= x2) and (y1 <= y <= y2)
            
            if center_in_target:
                cv2.putText(frame, "CIRCLE DETECTED", (x1 + 10, y1 + 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2) 
                square_color = (0, 0, 255) 

            print(f"Обнаружен круг: Центр=({x}, {y}), Радиус={r}, В центре: {center_in_target}")

        cv2.rectangle(frame, (x1, y1), (x2, y2), square_color, 2)
        return frame

    def run(self):
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Не удалось прочитать кадр, завершение работы.")
                break

            height, width = frame.shape[:2]
            xcenter, ycenter = width // 2, height // 2

            # Вычисляем координаты центрального квадрата
            half_square = self.target_square_size // 2
            square_x1 = xcenter - half_square
            square_y1 = ycenter - half_square
            square_x2 = xcenter + half_square
            square_y2 = ycenter + half_square
            target_area_coords = (square_x1, square_y1, square_x2, square_y2)

            processed_frame = self._preprocess_frame(frame.copy())
            circles = self._find_circles(processed_frame)

            # Если найдено несколько кругов, работаем с первым
            detected_circle_info = circles[0] if circles is not None and len(circles) > 0 else None

            # Отрисовываем оверлей кадра
            output_frame = self._draw_overlays(frame, detected_circle_info, target_area_coords)

            cv2.imshow('Detector', output_frame) # Изменил название окна

            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("Завершение работы по запросу пользователя.")
                break

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    tracker = CircleTracker(camera_index=0, target_square_size=200)
    try:
        tracker.run()
    except IOError as e:
        print(f"Ошибка инициализации камеры: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")