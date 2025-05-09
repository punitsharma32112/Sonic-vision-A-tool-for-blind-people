import cv2
import easyocr

# Initialize OCR reader
reader = easyocr.Reader(['en', 'hi'], recog_network='english_g2')

def extract_text(frame):
    # Convert frame to grayscale for better OCR accuracy
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(gray, (640, 480))

    result = reader.readtext(resized)
    return " ".join([entry[1] for entry in result]) if result else None
