from pathlib import Path
from datetime import datetime


def get_today_str() -> str:
    """Get current date"""
    return datetime.now().strftime("%a %b %-d, %Y")

def get_current_dir() -> Path:
    try:
        return Path(__file__).resolve().parent
    except NameError:
        return Path.cwd()