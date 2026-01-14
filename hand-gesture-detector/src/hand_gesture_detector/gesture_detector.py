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
            g = self.detect_thumb_gesture(hand)

            if g == "up":
                return "up"
            if g == "down":
                has_thumb_down = True

        if has_thumb_down:
            return "down"

        return None
