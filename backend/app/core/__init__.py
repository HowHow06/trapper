from .config import Settings
from pathlib import Path
import os

dev_path = Path(__file__).resolve().parent.parent.parent.parent / ".env"
settings = Settings(_env_file=dev_path, _env_file_encoding='utf-8')
