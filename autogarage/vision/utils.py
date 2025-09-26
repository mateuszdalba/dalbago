import cv2
import easyocr
from PIL import Image

# Do not initialize here
_reader = None

def get_reader():
    global _reader
    if _reader is None:
        # Initialize only once, when first needed
        _reader = easyocr.Reader(['en'])
    return _reader

def detect_plate_from_image(image_path: str):
    """Run OCR on given image file and return best candidate plate"""
    reader = get_reader()
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    results = reader.readtext(gray)
    candidates = []

    for (bbox, text, prob) in results:
        plate_candidate = text.strip().replace(" ", "").upper()
        if 4 <= len(plate_candidate) <= 8 and prob > 0.5:
            candidates.append((plate_candidate, prob))

    # pick best candidate
    if not candidates:
        return None
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0][0]
