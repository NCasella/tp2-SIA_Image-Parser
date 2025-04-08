import json

config = {}

# this file is used as a global state for all the other files without circular dependencies
def init_config(file_path: str):
    global config
    with open(file_path) as config_file:
        config_data = json.load(config_file)
    for key, value in config_data.items():
        config[key] = value