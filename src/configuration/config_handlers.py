import json


def config_load(config_path):
    with open(config_path, 'r') as file:
        config_data = json.load(file)

    return config_data 


default_config = config_load("src/configuration/schema/default_config.json") 
user_config = config_load("src/configuration/schema/user_config.json") 

def config(field,config_model = "default_model"):

    config_model_map = {
        "default" : "default_model",
        "user" : "user_model"
    }

    model_use = config_model_map.get(config_model, "default_model")

    if model_use == "default_model":
        from .model_handlers import default_model
        config_model = default_model
    else:
        from .model_handlers import user_model
        config_model = user_model


    config_dict = {
        "default_camera" : config_model.camera_properties.DEFAULT_CAMERA,
        "frame_width" : config_model.camera_properties.FRAME_WIDTH,
        "frame_height" : config_model.camera_properties.FRAME_HEIGHT,
        "fps" : config_model.camera_properties.FPS,
        "brightness" : config_model.camera_properties.BRIGHTNESS,
        "contrast" : config_model.camera_properties.CONTRAST,
        "saturation" : config_model.camera_properties.SATURATION,
        "hue" : config_model.camera_properties.HUE,
        "gain" : config_model.camera_properties.GAIN,
        "exposure" : config_model.camera_properties.EXPOSURE,
        "orientation" : config_model.frames.ORIENTATION.value,
        "flip_direction" : config_model.frames.FLIP_DIRECTION.value,
        "frame_format" : config_model.frames.FRAME_FORMAT.value,
        "use_static_mode" : config_model.handTracking.USE_STATIC_MODE,
        "max_hands_count" : config_model.handTracking.MAX_HANDS_COUNT,
        "min_detection_threshold" : config_model.handTracking.MIN_DETECTION_THRESHOLD,
        "min_tracking_threshold" : config_model.handTracking.MIN_TRACKING_THRESHOLD,
    }

    value = config_dict.get(field, None)

    return value


if __name__ == "__main__":
   # test
   print(config("frame_width", "default"))
   print(type(config("use_static_mode")))
   print(type(config("max_hands_count")))
   print(type(config("min_detection_threshold")))
   print(type(config("min_tracking_threshold")))
   print(config("use_static_mode"))
   print(config("max_hands_count"))
   print(config("min_detection_threshold"))
   print(config("min_tracking_threshold"))
