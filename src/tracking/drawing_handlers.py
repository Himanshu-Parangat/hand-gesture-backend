class LandmarksDraw:
    def __init__(self):
        self.drawing_solution = mp.solutions.draw_landmarks
        self.hand_connections = self.hand_solution.HAND_CONNECTIONS

    def draw_landmarks(self, frames, hand_landmarks):
        drawn_frame = frames.copy()
        self.drawing_solution.draw_landmarks(
            drawn_frame,
            hand_landmarks,
            self.hand_connections,
            self.drawing_solution.DrawingSpec(color=(255, 255, 255), thickness=2, circle_radius=2),
            self.drawing_solution.DrawingSpec(color=(0, 0, 0), thickness=2)
        )
        return drawn_frame

