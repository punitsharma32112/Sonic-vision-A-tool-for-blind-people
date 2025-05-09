import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self, maxHands=1, detectionCon=0.7, trackCon=0.6, smoothing=0.7):
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            max_num_hands=maxHands,
            min_detection_confidence=detectionCon,
            min_tracking_confidence=trackCon
        )
        self.mpDraw = mp.solutions.drawing_utils
        self.tipIds = [4, 8, 12, 16, 20]  # Thumb & fingertips (index, middle, ring, pinky)
        self.smooth_fingertip = None  # For smoothing
        self.smoothing_factor = smoothing  # Adjustable smoothing

    def find_hands(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpHands.HAND_CONNECTIONS)
        return self.results

    def is_pointing(self, img):
        """Detect if the user is pointing and return the fingertip position."""
        self.find_hands(img)
        if not self.results.multi_hand_landmarks:
            return None

        handLms = self.results.multi_hand_landmarks[0]
        lmList = [(int(lm.x * img.shape[1]), int(lm.y * img.shape[0])) for lm in handLms.landmark]

        index_tip, index_dip = lmList[8], lmList[7]
        middle_mcp = lmList[9]  # Base of middle finger (palm reference)

        # Ensure the index finger is pointing (extended) while other fingers are folded
        if not self._is_index_pointing(lmList):
            return None

        # Apply exponential smoothing
        fingertip = np.array(index_tip, dtype=np.float32)
        if self.smooth_fingertip is None:
            self.smooth_fingertip = fingertip
        else:
            self.smooth_fingertip = (
                self.smoothing_factor * self.smooth_fingertip + (1 - self.smoothing_factor) * fingertip
            )

        return tuple(map(int, self.smooth_fingertip))

    def _is_index_pointing(self, lmList):
        """Checks if only the index finger is extended while others are folded."""
        index_tip, index_dip = lmList[8], lmList[7]
        middle_tip, middle_pip = lmList[12], lmList[10]
        ring_tip, ring_pip = lmList[16], lmList[14]
        pinky_tip, pinky_pip = lmList[20], lmList[18]

        # Index finger must be straight (tip above DIP joint)
        if index_tip[1] > index_dip[1]:
            return False

        # Other fingers must be bent (tip below PIP joint)
        if middle_tip[1] < middle_pip[1] or ring_tip[1] < ring_pip[1] or pinky_tip[1] < pinky_pip[1]:
            return False

        return True
