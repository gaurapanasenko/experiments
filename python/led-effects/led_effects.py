import cv2
import numpy as np
import time
from typing import List

from nptyping import NDArray

ColorType = NDArray[(3,), np.uint8]
Zled = List[NDArray]
BLUE = np.array([255, 0, 0], dtype=np.uint8)
GREEN = np.array([0, 255, 0], dtype=np.uint8)
RED = np.array([0, 0, 255], dtype=np.uint8)
BLACK = np.array([0, 0, 0], dtype=np.uint8)

class Segment:
    def __init__(self, group: int, start: int, end: int, colors: List[ColorType]) -> None:
        for i in range(len(colors), 3):
            colors.append(BLACK)
        self.group: int = group
        self.start: int = start
        self.end: int = end
        self.color: ColorType = colors

def static_effect(zled: Zled, segment: Segment, timestamp: float) -> Zled:
    zled[segment.group][segment.start:segment.end] = segment.color[0]
    return zled

def pulse_effect(zled: Zled, segment: Segment, timestamp: float) -> Zled:
    intensity = np.sin(timestamp * 4) / 2 + 0.5
    color = segment.color[0] * intensity
    zled[segment.group][segment.start:segment.end] = color
    return zled

def wave_effect(zled: Zled, segment: Segment, timestamp: float) -> Zled:
    diff = segment.end - segment.start
    one_width = diff // 8
    segm = zled[segment.group][segment.start:segment.end]
    segm[:] = BLACK
    coef = one_width
    colors = np.array(segment.color)
    for i, col in enumerate(segm):
        intensity = np.array([
            np.sin((i / one_width - timestamp) * np.pi) / 2 + 0.5,
            np.sin((i / one_width + 2/3 - timestamp) * np.pi) / 2 + 0.5,
            np.sin((i / one_width + 4/3 - timestamp) * np.pi) / 2 + 0.5,
        ])
        col[:] = sum(intensity * colors)
    return zled

def pulse_wave_effect(zled: Zled, segment: Segment, timestamp: float) -> Zled:
    glob_inensity = np.sin(timestamp * 4) / 2 + 0.5
    diff = segment.end - segment.start
    one_width = diff // 8
    segm = zled[segment.group][segment.start:segment.end]
    segm[:] = BLACK
    coef = one_width
    colors = np.array(segment.color)
    for i, col in enumerate(segm):
        intensity = np.array([
            np.sin((i / one_width - timestamp) * np.pi) / 2 + 0.5,
            np.sin((i / one_width + 2/3 - timestamp) * np.pi) / 2 + 0.5,
            np.sin((i / one_width + 4/3 - timestamp) * np.pi) / 2 + 0.5,
        ])
        col[:] = sum(intensity * glob_inensity * colors)
    return zled

def shift_effect(zled: Zled, segment: Segment, timestamp: float) -> Zled:
    diff = segment.end - segment.start
    one_width = diff // 8
    segm = zled[segment.group][segment.start:segment.end]
    segm[:] = BLACK
    coef = one_width
    for i, col in enumerate(segm):
        col_id = ((i - int(timestamp * 8)) // one_width) % 3
        col[:] = segment.color[col_id]
    return zled

def test_effects() -> None:
    strip = np.zeros((10, 40, 3), dtype=np.uint8)
    while True:
        timestamp = time.time()
        strip[4][39] = RED
        strip = static_effect(strip, Segment(4, 0, 40, [GREEN]), timestamp)
        strip = pulse_wave_effect(strip, Segment(5, 0, 39, [BLUE, GREEN, RED]), timestamp)
        strip = pulse_effect(strip, Segment(6, 0, 40, [GREEN]), timestamp)
        strip = wave_effect(strip, Segment(7, 0, 39, [BLUE, GREEN, RED]), timestamp)
        strip = shift_effect(strip, Segment(8, 0, 39, [GREEN, BLACK, BLUE]), timestamp)
        strip_out = cv2.resize(strip, (1000, 1000//4), interpolation=cv2.INTER_NEAREST)
        cv2.imshow("img", strip_out)
        cv2.waitKey(10)

if __name__ == "__main__":
    test_effects()

