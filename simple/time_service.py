from datetime import datetime

def is_office_open() -> bool:
    now = datetime.now()
    return 9 <= now.hour < 18