# ==========================================
# utils/logger.py
# ==========================================

import os
from datetime import datetime

LOG_FILE = "logs/activity.log"


def log_activity(action):

    os.makedirs("logs", exist_ok=True)

    current_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")

    with open(LOG_FILE, "a", encoding="utf-8") as file:

        file.write(f"[{current_time}] {action}\n")