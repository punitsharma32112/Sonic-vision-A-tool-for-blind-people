from scripts.handtracking import HandTracker
from scripts.object_detection import ObjectDetector

class ObjectPointer:
    def __init__(self):
        self.hand_tracker = HandTracker()
        self.object_detector = ObjectDetector()

    def find_pointed_object(self, frame):
        fingertip = self.hand_tracker.is_pointing(frame)
        if fingertip is None:
            return None, None  # No valid pointing detected

        detected_objects = self.object_detector.detect_objects(frame)
        if not detected_objects:
            return None, fingertip  # No objects detected

        pointed_object = self.get_pointed_object(fingertip, detected_objects)
        return pointed_object, fingertip

    def get_pointed_object(self, fingertip, detected_objects):
        for obj in detected_objects:
            x1, y1, x2, y2 = obj['bbox']
            if x1 <= fingertip[0] <= x2 and y1 <= fingertip[1] <= y2:
                return obj  # If fingertip is inside bounding box, return object
        
        return None
