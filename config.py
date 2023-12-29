from dotenv import dotenv_values
from pathlib import Path
config = dotenv_values(f"{Path.home()}/GIT/UTorontoEmgAI/.env")

def get(config_field: str):
    return config[config_field]
