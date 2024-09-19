import tensorflow as tf
from tensorflow.keras.models import load_model # type: ignore
import numpy as np
import cv2

model = load_model('greek_letter_recognition_model.h5')

# Funkcja do przetwarzania ręcznie narysowanego obrazu
def preprocess_image(image):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # Konwersja do skali szarości
    image = cv2.resize(image, (45, 45))  # Zmiana rozmiaru obrazu na 45x45 piksele
    image = image.reshape(1, 45, 45, 1)  # Dopasowanie kształtu (batch_size=1, 45x45, 1 kanał)
    image = image / 255.0  # Normalizacja obrazu
    return image


def draw_symbol():
    canvas = np.ones((500, 500, 3), dtype="uint8") * 255
    drawing = False
    last_point = None  # przechowanie poprzedniej pozycji kursora

    def drawOnMouseClickEvent(event, x, y, flags, param):
        nonlocal drawing, last_point

        if event == cv2.EVENT_LBUTTONDOWN:  
            drawing = True
            last_point = (x, y)
        elif event == cv2.EVENT_MOUSEMOVE and drawing:  # rysowanie przy przesuwaniu myszy
            if last_point is not None:
                cv2.line(canvas, last_point, (x, y), (0, 0, 0), 5)
            last_point = (x, y)
        elif event == cv2.EVENT_LBUTTONUP:  # Koniec rysowania
            drawing = False
            last_point = None

  
    cv2.namedWindow("Rysuj literę")
    cv2.setMouseCallback("Rysuj literę", drawOnMouseClickEvent)

    while True:
        cv2.imshow("Rysuj literę", canvas)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    cv2.destroyAllWindows()
    return canvas


user_image = draw_symbol()
preprocessed_image = preprocess_image(user_image)

prediction = model.predict(preprocessed_image)
predicted_class = np.argmax(prediction)

greek_letters = ['Alpha', 'Beta', 'Delta', 'Phi', 'Sigma']

print(f"Rozpoznana litera grecka: {greek_letters[predicted_class]}")
