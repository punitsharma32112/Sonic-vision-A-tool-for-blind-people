import cv2

def open_camera():
    cap = cv2.VideoCapture(1)
    return cap if cap.isOpened() else None

def capture_frame(cap):
    # Read multiple frames to flush buffer (optional but helps ensure freshness)
    for _ in range(5):
        ret, frame = cap.read()
    if ret:
        return frame
    else:
        return None