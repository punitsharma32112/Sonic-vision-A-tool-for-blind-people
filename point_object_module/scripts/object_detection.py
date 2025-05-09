import cv2
from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path="./models/yolov8n.pt", confidence_threshold=0.4, exclude_classes=None):
        self.model = YOLO(model_path)
        self.confidence_threshold = confidence_threshold
        self.exclude_classes = set(exclude_classes) if exclude_classes else set()

    def detect_objects(self, frame, fingertip=None, hand_bbox=None):
        results = self.model(frame, imgsz=960)  # Higher resolution improves small-object detection
        detections = []

        for result in results:
            boxes = result.boxes.xyxy  # Bounding boxes
            confidences = result.boxes.conf  # Confidence scores
            class_ids = result.boxes.cls  # Class labels

            for box, conf, cls in zip(boxes, confidences, class_ids):
                if conf < self.confidence_threshold:
                    continue  # Ignore weak detections

                label = result.names[int(cls)]
                if label in self.exclude_classes:
                    continue  # Skip excluded objects

                x1, y1, x2, y2 = map(int, box)

                # Ignore objects inside or very close to the hand bounding box
                if hand_bbox and self.is_inside_hand((x1, y1, x2, y2), hand_bbox):
                    continue  

                # Ensure detection is **above** the fingertip
                if fingertip and y2 > fingertip[1]:  
                    continue  

                # Allow small objects to be detected
                width, height = x2 - x1, y2 - y1
                if width < 15 or height < 15:  # Fine-tuned for small objects
                    continue  

                detections.append({'bbox': (x1, y1, x2, y2), 'label': label, 'confidence': float(conf)})

        # Apply Non-Maximum Suppression (NMS) to remove duplicate overlapping boxes
        detections = self.apply_nms(detections)

        return detections

    def is_inside_hand(self, object_bbox, hand_bbox, margin=10):

        x1, y1, x2, y2 = object_bbox
        hx1, hy1, hx2, hy2 = hand_bbox

        # Expand hand box slightly to ensure objects near the hand are also ignored
        hx1 -= margin
        hy1 -= margin
        hx2 += margin
        hy2 += margin

        # Check if object is inside or overlapping the hand region
        if hx1 <= x1 <= hx2 and hy1 <= y1 <= hy2:
            return True
        if hx1 <= x2 <= hx2 and hy1 <= y2 <= hy2:
            return True

        return False

    def apply_nms(self, detections, iou_threshold=0.4):
        if not detections:
            return []

        boxes = [d["bbox"] for d in detections]
        confidences = [d["confidence"] for d in detections]

        indices = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence_threshold, iou_threshold)
        return [detections[i] for i in indices.flatten()] if len(indices) > 0 else []
