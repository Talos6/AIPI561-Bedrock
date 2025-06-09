import yaml
from loguru import logger

class ConfigLoader:
    def __init__(self):
        self.config = self._load_config()
    
    def _load_config(self):
        try:
            with open('config.yaml', 'r') as file:
                config = yaml.safe_load(file)
                logger.info(f"Configuration loaded from config.yaml")
                return config
        except Exception as e:
            logger.error(f"Error loading configuration: {e}")
            raise

_config_instance = None

def get_config():
    global _config_instance
    if _config_instance is None:
        _config_instance = ConfigLoader()
    return _config_instance.config