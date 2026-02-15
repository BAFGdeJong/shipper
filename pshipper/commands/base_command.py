from pathlib import Path

from pshipper.commands.config import Config


class BaseCommand:
    def __init__(self, config: Config):
        self.config = config

    def get_data_file(self, filename: str) -> Path:
        return self.config.data_path / filename