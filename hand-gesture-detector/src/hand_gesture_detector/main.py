import cv2
import time
from hand_gesture_detector.config import AppConfig
from hand_gesture_detector.detector import HandDetector
from hand_gesture_detector.visualizer import FrameDrawer
from hand_gesture_detector.gesture_detector import GestureDetector


def main():
    config = AppConfig()
    detector = HandDetector(config)
    drawer = FrameDrawer()
    gesture_detector = GestureDetector()

    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.cam_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.cam_height)

    if not cap.isOpened():
        print("Error: Could not open webcam.")
        return

    print("System Started. Press 'Q' to exit.")

    prev_time = time.time()

    try:
        while True:
            success, frame = cap.read()
            if not success:
                print("Camera frame drop.")
                break

            timestamp_ms = int(time.time() * 1000)
            detector.detect_async(frame, timestamp_ms)

            result = detector.get_latest_result()

            drawer.draw_landmarks(frame, result)

            gesture = (gesture_detector.detect_global_gesture(result.hand_landmarks) if result and result.hand_landmarks else None)
            drawer.draw_gesture_indicator(frame, gesture)

            curr_time = time.time()
            fps = 1 / (curr_time - prev_time) if (curr_time - prev_time) > 0 else 0
            prev_time = curr_time

            num_hands = (
                len(result.hand_landmarks) if result and result.hand_landmarks else 0
            )
            drawer.draw_status(frame, fps, num_hands)

            cv2.imshow("Hand Gesture System", frame)

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        detector.close()
        cap.release()
        cv2.destroyAllWindows()
