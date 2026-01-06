from dataclasses import dataclass


@dataclass(frozen=True)
class AppConfig:
    model_path: str = "models/hand_landmarker.task"
    num_hands: int = 2
    detection_interval_ms: int = 50
    cam_width: int = 640
    cam_height: int = 480
    cam_fps: int = 30
