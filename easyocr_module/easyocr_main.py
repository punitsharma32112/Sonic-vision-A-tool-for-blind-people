import os
import sys
import time
import cv2

# ─── Ensure we’re in module directory ─────────────────────────────────────────
script_dir = os.path.dirname(os.path.abspath(__file__))
os.chdir(script_dir)

from camera import open_camera, capture_frame
from ocr    import extract_text
from speech import speak_text

# ─── Constants ────────────────────────────────────────────────────────────────
CAPTURE_FILE = "capture_trigger.txt"
STOP_FILE    = "stop_ocr.txt"
PAGE_FOLDER  = "pages"

# ─── Setup ─────────────────────────────────────────────────────────────────────
os.makedirs(PAGE_FOLDER, exist_ok=True)
cap = open_camera()
if not cap:
    speak_text("Unable to access the camera. Exiting.", "en")
    sys.exit(1)

speak_text("Book Reader active", "en")
page_counter = 1

# ─── Main Loop ────────────────────────────────────────────────────────────────
while True:
    # stop trigger
    if os.path.exists(STOP_FILE):
        speak_text("Text reader stopped.", "en")
        os.remove(STOP_FILE)
        break

    # capture trigger
    if os.path.exists(CAPTURE_FILE):
        os.remove(CAPTURE_FILE)
        print(f"[OCR] Capturing frame for Page {page_counter}…")
        frame = capture_frame(cap)
        if frame is None:
            speak_text("Failed to capture frame. Check camera.", "en")
            continue

        text = extract_text(frame)
        if text:
            fn = os.path.join(PAGE_FOLDER, f"page{page_counter}.txt")
            with open(fn, "w", encoding="utf-8") as f:
                f.write(text)
            print(f"[OCR] Saved text to {fn}")
            speak_text(f"Page {page_counter} saved.", "en")
            page_counter += 1
        else:
            speak_text("No text detected. Please adjust the camera.", "en")

    time.sleep(0.2)

# ─── Cleanup ───────────────────────────────────────────────────────────────────
cap.release()
cv2.destroyAllWindows()
