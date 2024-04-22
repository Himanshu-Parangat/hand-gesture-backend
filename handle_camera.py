import cv2

class Camera:
    def __init__(self):
        self.camera_index = 0
        self.camera_feed = cv2.VideoCapture(self.camera_index)

        self.properties = {
            'FRAME_WIDTH': cv2.CAP_PROP_FRAME_WIDTH,
            'FRAME_HEIGHT': cv2.CAP_PROP_FRAME_HEIGHT,
            'FPS': cv2.CAP_PROP_FPS,
            'BRIGHTNESS': cv2.CAP_PROP_BRIGHTNESS,
            'CONTRAST': cv2.CAP_PROP_CONTRAST,
            'SATURATION': cv2.CAP_PROP_SATURATION,
            'HUE': cv2.CAP_PROP_HUE,
            'GAIN': cv2.CAP_PROP_GAIN,
            'EXPOSURE': cv2.CAP_PROP_EXPOSURE
        }

    def capture_frame(self, orientation, flip_direction, frame_format):

        isFrameRead = self.camera_feed.read()[0]

        if isFrameRead:

            frames = self.camera_feed.read()[1]
            frames = self._rotate_frame(frames, orientation)
            frames = self._flip_frames(frames, flip_direction)
            frames,rgb_frames = self._change_color_space(frames, frame_format)
            processed_frames = frames
            processed_frames_rgb = rgb_frames

            return processed_frames, processed_frames_rgb
        else:
            self._empty_frames()

    @staticmethod
    def _rotate_frame(frames, orientation):
        if orientation == "clockwise":
            rotated_frames = cv2.rotate(frames, cv2.ROTATE_90_CLOCKWISE)
        elif orientation == "180":
            rotated_frames = cv2.rotate(frames, cv2.ROTATE_180)
        elif orientation == "counter-clockwise":
            rotated_frames = cv2.rotate(frames, cv2.ROTATE_90_COUNTERCLOCKWISE)
        else:
            rotated_frames = frames

        return rotated_frames

    @staticmethod
    def _flip_frames(frames, flip_direction):

        flip_map = {
            "horizontally": 1,
            "vertically": 0,
            "both": -1
        }

        flip_code = flip_map.get(flip_direction)

        if flip_code is None:
            flipped_frames = frames
        else:
            flipped_frames = cv2.flip(frames, flip_code)

        return flipped_frames


    @staticmethod
    def _change_color_space(frames, frame_format):

        converted_frames_rgb = cv2.cvtColor(frames, cv2.COLOR_BGR2RGB)

        color_space_map = {
            "RGB": converted_frames_rgb,
            "HSV": cv2.cvtColor(frames, cv2.COLOR_BGR2HSV),
            "HLS": cv2.cvtColor(frames, cv2.COLOR_BGR2HLS),
            "GRAY": cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
        }

        if frame_format in color_space_map:
            converted_frames = color_space_map[frame_format]
        else:
            converted_frames = frames

        return converted_frames, converted_frames_rgb


    @staticmethod
    def _empty_frames():
       raise RuntimeError("No frames were read from the camera. Please check your device.")
