import cv2
import os

def detect_whiteboard(image_path):
    
    """
    Wykrywa kontury tablicy w obrazie i zwraca listę ich współrzędnych.

    Args:
        image_path (str): Ścieżka do obrazu, w którym ma być wykryta tablica.

    Returns:
        list: Lista prostokątnych konturów tablicy, gdzie każdy kontur jest reprezentowany jako 
              tuple (x, y, w, h), gdzie:
              - x, y: Współrzędne lewego górnego rogu prostokąta
              - w, h: Szerokość i wysokość prostokąta.
    """
    
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)

    _, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    whiteboard_contours = []
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:  
            x, y, w, h = cv2.boundingRect(approx)
            if w > 500 and h > 300:  
                whiteboard_contours.append((x, y, w, h))

    return whiteboard_contours


def crop_and_save_whiteboard(image_path, output_path, contours, name):
    
    """
    Wycina tablice z obrazu na podstawie przekazanych konturów i zapisuje je jako osobne pliki.

    Args:
        image_path (str): Ścieżka do obrazu źródłowego.
        output_path (str): Ścieżka do katalogu, w którym zostaną zapisane wycięte tablice.
        contours (list): Lista konturów tablicy, gdzie każdy kontur jest tuplem (x, y, w, h).
        name (str): Nazwa bazowa używana do generowania nazw plików wyjściowych.

    Returns:
        None: Funkcja zapisuje wycięte tablice jako osobne obrazy w podanym katalogu.
    """
    
    image = cv2.imread(image_path)
    for i, (x, y, w, h) in enumerate(contours):
        if w < 50 or h < 50:  
            print(f"Skipping small contour: x={x}, y={y}, w={w}, h={h}")
            continue
        cropped = image[y:y+h, x:x+w]
        cv2.imwrite(f"{output_path}/whiteboard_{name}_{i}.png", cropped)
        
def preprocess_for_ocr(image_path):
    
    """
    Przygotowuje obraz do przetwarzania OCR, wykonując binarizację i operację morfologiczną.

    Args:
        image_path (str): Ścieżka do obrazu, który ma zostać przygotowany.

    Returns:
        numpy.ndarray: Przetworzony obraz w skali szarości po operacjach binarizacji i otwarcia morfologicznego.

    Raises:
        ValueError: Jeśli ścieżka obrazu jest nieprawidłowa lub plik nie istnieje.
    """
        
    if not isinstance(image_path, str) or not os.path.exists(image_path):
        raise ValueError(f"Invalid image path: {image_path}")
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    _, binary = cv2.threshold(image, 150, 255, cv2.THRESH_BINARY)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    opened = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel)
    return opened