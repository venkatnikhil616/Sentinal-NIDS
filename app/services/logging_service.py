import json
import os
from datetime import datetime
from flask import current_app

from database.crud import insert_log


def log_event(event_type: str, data: dict, result: dict):
    """
    Central logging function for all system events
    """
    try:
        log_entry = build_log_entry(event_type, data, result)

        # STORE IN DATABASE
  
        try:
            insert_log(log_entry)
        except Exception as db_error:
            current_app.logger.error(f"[DB LOG ERROR] {str(db_error)}")

        # STORE IN FILE
      
        try:
            log_to_file(log_entry)
        except Exception as file_error:
            current_app.logger.error(f"[FILE LOG ERROR] {str(file_error)}")

    except Exception as e:
        current_app.logger.error(f"[LOGGING ERROR] {str(e)}")

# BUILD LOG ENTRY

def build_log_entry(event_type, data, result):
    return {
        "timestamp": datetime.utcnow().isoformat(),
        "event_type": event_type,
        "input_data": data,
        "prediction": result.get("label"),
        "attack_type": result.get("attack_type"),
        "confidence": result.get("confidence"),
        "raw_result": result
    }


# FILE LOGGING

def log_to_file(log_entry):
    try:
        config = current_app.config if current_app else None

        if config:
            log_file = config.get("LOG_FILE", "logs/system.log")
        else:
            log_file = "logs/system.log"

        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        with open(log_file, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

    except Exception as e:
        current_app.logger.error(f"[FILE LOG ERROR] {str(e)}")
