import json
from pprint import pprint 


def config_load(config_path):
    with open(config_path, 'r') as file:
        config_data = json.load(file)

    return config_data 


default_config = config_load("./config/default_config.json") 
user_config = config_load("./config/user_config.json") 


if __name__ == "__main__":
   pprint(default_config["frames"]["ORIENTATION"]) 
