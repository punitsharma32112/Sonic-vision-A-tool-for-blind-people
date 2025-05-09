import os
import cv2
import threading
import time
from scripts.integration import ObjectPointer
from scripts.audio_feedback import AudioFeedback

# Constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STOP_FILE = os.path.abspath(os.path.join(BASE_DIR, "..", "stop_pointer.txt"))
DETECTION_DELAY  = 1  # seconds

# Globals
cap               = cv2.VideoCapture(1)
object_pointer    = ObjectPointer()
audio_feedback    = AudioFeedback()
latest_frame      = None
latest_detection  = None
lock              = threading.Lock()
last_label        = None
last_time         = 0

# Announce start
audio_feedback.speak("Point object detection started.")

def detect_objects():
    global latest_frame, latest_detection
    while True:
        with lock:
            frame = latest_frame
        if frame is None:
            time.sleep(0.01)
            continue
        obj, tip = object_pointer.find_pointed_object(frame.copy())
        with lock:
            latest_detection = (obj, tip)

def process_frames():
    global latest_frame, last_label, last_time

    try:
        while True:
            # Shutdown trigger
            if os.path.exists(STOP_FILE):
                os.remove(STOP_FILE)
                break

            ret, frame = cap.read()
            if not ret:
                print("Error: could not read frame.")
                break

            with lock:
                latest_frame = frame.copy()
                detection = latest_detection

            # Unpack detection
            pointed_object, fingertip = detection or (None, None)

            # Draw fingertip
            if fingertip:
                cv2.circle(frame, fingertip, 10, (0, 255, 0), -1)

            # Draw and speak object when stable
            if pointed_object:
                x1, y1, x2, y2 = pointed_object['bbox']
                label = pointed_object['label']
                cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
                cv2.putText(frame, label, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

                now = time.time()
                if label == last_label:
                    if now - last_time >= DETECTION_DELAY:
                        audio_feedback.speak(label)
                        last_time = now
                else:
                    last_label = label
                    last_time = now

            cv2.imshow("Object Pointer", frame)
            cv2.waitKey(1)

    finally:
        audio_feedback.speak("Point object detection stopped")
        time.sleep(2)  # Let the speech finish before closing windows
        cap.release()
        cv2.destroyAllWindows()

# Start detection thread and frame loop
threading.Thread(target=detect_objects, daemon=True).start()
process_frames()