import cv2
import numpy as np
from mediapipe.tasks.python import vision


class FrameDrawer:
    HAND_CONNECTIONS: list[tuple[int, int]] = [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 4),  # Thumb
        (0, 5),
        (5, 6),
        (6, 7),
        (7, 8),  # Index
        (5, 9),
        (9, 10),
        (10, 11),
        (11, 12),  # Middle
        (9, 13),
        (13, 14),
        (14, 15),
        (15, 16),  # Ring
        (13, 17),
        (17, 18),
        (18, 19),
        (19, 20),  # Pinky
        (0, 17),  # Wrist
    ]

    def draw_landmarks(
        self, frame: np.ndarray, result: vision.HandLandmarkerResult
    ) -> None:
        if not result or not result.hand_landmarks:
            return

        height, width, _ = frame.shape

        for hand_landmarks in result.hand_landmarks:
            for p1_idx, p2_idx in self.HAND_CONNECTIONS:
                p1 = hand_landmarks[p1_idx]
                p2 = hand_landmarks[p2_idx]

                x1, y1 = int(p1.x * width), int(p1.y * height)
                x2, y2 = int(p2.x * width), int(p2.y * height)

                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            for landmark in hand_landmarks:
                cx, cy = int(landmark.x * width), int(landmark.y * height)
                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

    def draw_status(self, frame: np.ndarray, fps: float, hands_detected: int) -> None:
        status_color = (0, 255, 0) if hands_detected > 0 else (0, 0, 255)
        text = f"FPS: {fps:.1f} | Hands: {hands_detected}"
        cv2.putText(
            frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, status_color, 2
        )
    
    def draw_gesture_indicator(self, frame: np.ndarray, gesture: str | None) -> None:
        h, w, _ = frame.shape

        if gesture == "up":
            color, label = (0, 255, 0), "THUMB UP"
        elif gesture == "down":
            color, label = (0, 0, 255), "THUMB DOWN"
        elif gesture == "heart":
            color, label = (255, 0, 255), "HEART"
        elif gesture == "palm":
            color, label = (0, 255, 255), "OPEN PALM"
        elif gesture == "fist":
            color, label = (0, 0, 150), "FIST"
        elif gesture == "peace":
            color, label = (255, 100, 0), "PEACE"
        elif gesture == "ok":
            color, label = (100, 255, 100), "OK"
        else:
            color, label = (150, 150, 150), "NO GESTURE"

        cv2.rectangle(frame, (w - 120, 20), (w - 20, 120), color, -1)
        cv2.putText(
            frame, label, (w - 170, 150),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2
        )