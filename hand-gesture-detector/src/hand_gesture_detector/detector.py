import cv2
import threading
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
from typing import Optional
from hand_gesture_detector.config import AppConfig


class HandDetector:
    def __init__(self, config: AppConfig) -> None:
        self.config = config
        self._lock = threading.Lock()
        self._latest_result: Optional[vision.HandLandmarkerResult] = None
        self._last_timestamp_ms: int = 0

        base_options = python.BaseOptions(model_asset_path=config.model_path)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.LIVE_STREAM,
            num_hands=config.num_hands,
            result_callback=self._result_callback,
        )
        self.landmarker = vision.HandLandmarker.create_from_options(options)

    def _result_callback(
        self,
        result: vision.HandLandmarkerResult,
        output_image: mp.Image,
        timestamp_ms: int,
    ) -> None:
        with self._lock:
            self._latest_result = result

    def detect_async(self, frame_bgr: np.ndarray, timestamp_ms: int) -> None:
        if timestamp_ms - self._last_timestamp_ms < self.config.detection_interval_ms:
            return

        self._last_timestamp_ms = timestamp_ms

        frame_rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        self.landmarker.detect_async(mp_image, timestamp_ms)

    def get_latest_result(self) -> Optional[vision.HandLandmarkerResult]:
        with self._lock:
            return self._latest_result

    def close(self) -> None:
        self.landmarker.close()
