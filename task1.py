import cv2

def image_processing():
    img = cv2.imread('images/variant-3.jpeg')

    # Проверяем, удалось ли загрузить изображение
    if img is None:
        print("Ошибка: Изображение не найдено или не может быть загружено.")
        return


    height, width, _ = img.shape


    new_width = width // 3
    new_height = height // 3

    # Уменьшим изображение 
    resized_img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # Преобразуем уменьшенное изображение в HSV
    hsv_img = cv2.cvtColor(resized_img, cv2.COLOR_BGR2HSV)

    # Отображение
    cv2.imshow('Original (BGR) - Resized', resized_img)
    cv2.imshow('HSV Image - Resized', hsv_img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    image_processing()