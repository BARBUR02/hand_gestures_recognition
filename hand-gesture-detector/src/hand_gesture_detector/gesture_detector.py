import math
from typing import Optional


class GestureDetector:
    def _dist(self, p1, p2) -> float:
        return math.hypot(p1.x - p2.x, p1.y - p2.y)

    def detect_thumb_gesture(self, hand_landmarks) -> Optional[str]:
        thumb_mcp = hand_landmarks[2]
        thumb_tip = hand_landmarks[4]

        threshold = 0.05

        if thumb_tip.y < thumb_mcp.y - threshold:
            return "up"
        elif thumb_tip.y > thumb_mcp.y + threshold:
            return "down"

        return None

    def detect_shape_gesture(self, hand_landmarks) -> Optional[str]:
        # Finger tip indices: index(8), middle(12), ring(16), pinky(20)
        # Finger PIP indices: index(6), middle(10), ring(14), pinky(18)
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]

        wrist = hand_landmarks[0]
        extended = []
        for tip, pip in zip(tips, pips):
            # Check if finger is extended (distance from tip to wrist > distance from PIP joint to wrist)
            is_ext = self._dist(hand_landmarks[tip], wrist) > self._dist(hand_landmarks[pip], wrist)
            extended.append(is_ext)

        # 1. PALM (All fingers extended)
        if all(extended):
            return "palm"

        # 2. FIST (All fingers folded)
        if not any(extended):
            return "fist"

        # 3. PEACE (Index and middle extended, ring and pinky folded)
        if extended == [True, True, False, False]:
            return "peace"

        # 4. OK (Thumb and index touch, other fingers extended)
        thumb_tip = hand_landmarks[4]
        index_tip = hand_landmarks[8]
        if self._dist(thumb_tip, index_tip) < 0.05 and extended[1] and extended[2] and extended[3]:
            return "ok"

        return None

    def detect_heart_gesture(self, hands_landmarks) -> bool:
        if len(hands_landmarks) != 2:
            return False

        h1, h2 = hands_landmarks

        h1_thumb, h2_thumb = h1[4], h2[4]
        h1_index, h2_index = h1[8], h2[8]

        thumb_dist = self._dist(h1_thumb, h2_thumb)
        index_dist = self._dist(h1_index, h2_index)

        spread_1 = self._dist(h1[4], h1[8])
        spread_2 = self._dist(h2[4], h2[8])

        thumbs_close = thumb_dist < 0.12
        indexes_close = index_dist < 0.12
        fingers_spread = spread_1 > 0.08 and spread_2 > 0.08

        return thumbs_close and indexes_close and fingers_spread

    def hands_are_close(self, hands_landmarks) -> bool:
        if len(hands_landmarks) < 2:
            return False

        w1 = hands_landmarks[0][0]
        w2 = hands_landmarks[1][0]

        return self._dist(w1, w2) < 0.25

    def detect_global_gesture(self, hands_landmarks) -> Optional[str]:
        if self.detect_heart_gesture(hands_landmarks):
            return "heart"

        if len(hands_landmarks) >= 2 and self.hands_are_close(hands_landmarks):
            return None

        has_thumb_down = False

        for hand in hands_landmarks:
            # Check for thumb up/down first
            thumb_g = self.detect_thumb_gesture(hand)
            if thumb_g == "up":
                return "up"
            if thumb_g == "down":
                has_thumb_down = True

            # Check for other shapes
            shape_g = self.detect_shape_gesture(hand)
            if shape_g:
                return shape_g

        if has_thumb_down:
            return "down"

        return None
