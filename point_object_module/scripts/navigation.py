import numpy as np

class Navigator:
    def __init__(self, frame_width, frame_height):
        self.frame_width = frame_width
        self.frame_height = frame_height

    def get_navigation_instruction(self, fingertip, bbox):
        fx, fy = fingertip
        x1, y1, x2, y2 = bbox
        obj_center_x = (x1 + x2) // 2
        obj_center_y = (y1 + y2) // 2

        horizontal_offset = obj_center_x - fx
        vertical_offset = obj_center_y - fy
        distance = np.sqrt((obj_center_x - fx) ** 2 + (obj_center_y - fy) ** 2)

        # Estimate direction
        if abs(horizontal_offset) < self.frame_width * 0.1:
            direction = "straight"
        elif horizontal_offset > 0:
            direction = "to the right"
        else:
            direction = "to the left"

        # Estimate step count based on vertical offset
        steps = max(1, int(abs(vertical_offset) / (self.frame_height * 0.1)))
        return f"Take {steps} step{'s' if steps > 1 else ''} forward and slightly {direction}."
