from datetime import datetime


def get_today_str() -> str:
    """Get current date"""
    return datetime.now().strftime("%a %b %-d, %Y")
