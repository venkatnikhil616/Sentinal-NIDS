from typing import Dict, Any


class PreprocessingError(Exception):
    """Custom exception for preprocessing failures"""
    pass


# DEFAULT VALUES (NSL-KDD)

DEFAULT_VALUES = {
    "duration": 0,
    "protocol_type": "tcp",
    "service": "http",
    "flag": "SF",
    "src_bytes": 0,
    "dst_bytes": 0,
    "wrong_fragment": 0,
    "urgent": 0,
    "hot": 0,
    "num_failed_logins": 0,
    "logged_in": 0,
    "num_compromised": 0,
    "root_shell": 0,
    "su_attempted": 0,
    "num_root": 0,
    "num_file_creations": 0,
    "num_shells": 0,
    "num_access_files": 0,
    "num_outbound_cmds": 0,
    "is_host_login": 0,
    "is_guest_login": 0,
    "count": 0,
    "srv_count": 0,
    "serror_rate": 0.0,
    "srv_serror_rate": 0.0,
    "rerror_rate": 0.0,
    "srv_rerror_rate": 0.0,
    "same_srv_rate": 0.0,
    "diff_srv_rate": 0.0,
    "srv_diff_host_rate": 0.0
}


# ---------------------------
# HELPERS
# ---------------------------

def _safe_float(value, default=0.0):
    try:
        return float(value)
    except Exception:
        return default


def _safe_int(value, default=0):
    try:
        return int(float(value))
    except Exception:
        return default


def _safe_str(value, default=""):
    if value is None:
        return default
    return str(value).strip()


# ---------------------------
# MAIN PREPROCESS FUNCTION ✅ FIXED NAME
# ---------------------------

def preprocess(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate and clean incoming network data
    """

    if not isinstance(data, dict):
        raise PreprocessingError("Input must be a dictionary")

    processed = {}

    for key, default in DEFAULT_VALUES.items():
        raw_value = data.get(key, default)

        # TYPE HANDLING
        if isinstance(default, float):
            value = _safe_float(raw_value, default)

        elif isinstance(default, int):
            value = _safe_int(raw_value, default)

        elif isinstance(default, str):
            value = _safe_str(raw_value, default)

        else:
            value = raw_value

        # SANITY CHECK
        value = _apply_bounds(key, value)

        processed[key] = value

    return processed


# ---------------------------
# VALUE CHECKS
# ---------------------------

def _apply_bounds(key: str, value: Any):
    try:
        if key in ["duration", "src_bytes", "dst_bytes", "count", "srv_count"]:
            return max(0, value)

        if key.endswith("_rate"):
            return min(max(0.0, float(value)), 1.0)

        if key in ["logged_in", "is_host_login", "is_guest_login"]:
            return 1 if str(value).lower() in ["1", "true", "yes"] else 0

        return value

    except Exception:
        return 0
