from typing import Dict, List, Any

# FEATURE ORDER
# Must match training order
FEATURE_COLUMNS = [
    "duration",
    "protocol_type",
    "service",
    "flag",
    "src_bytes",
    "dst_bytes",
    "wrong_fragment",
    "urgent",
    "hot",
    "num_failed_logins",
    "logged_in",
    "num_compromised",
    "root_shell",
    "su_attempted",
    "num_root",
    "num_file_creations",
    "num_shells",
    "num_access_files",
    "num_outbound_cmds",
    "is_host_login",
    "is_guest_login",
    "count",
    "srv_count",
    "serror_rate",
    "srv_serror_rate",
    "rerror_rate",
    "srv_rerror_rate",
    "same_srv_rate",
    "diff_srv_rate",
    "srv_diff_host_rate"
]

# ENCODING MAPS

PROTOCOL_MAP = {
    "tcp": 0,
    "udp": 1,
    "icmp": 2
}

FLAG_MAP = {
    "SF": 0,
    "S0": 1,
    "REJ": 2,
    "RSTR": 3,
    "SH": 4,
    "RSTO": 5,
    "S1": 6,
    "S2": 7,
    "S3": 8,
    "OTH": 9
}

# NOTE: Services are many → fallback hashing
def encode_service(service: str) -> int:
    if not service:
        return 0
    return abs(hash(service)) % 1000  # bounded numeric

# MAIN FEATURE EXTRACTION

def extract_features(data: Dict[str, Any]) -> List[float]:
    """
    Convert raw network input into numerical feature vector
    """

    features = []

    for col in FEATURE_COLUMNS:
        value = data.get(col, 0)

        # HANDLE CATEGORICAL FIELDS

        if col == "protocol_type":
            value = PROTOCOL_MAP.get(str(value).lower(), 0)

        elif col == "flag":
            value = FLAG_MAP.get(str(value).upper(), 0)

        elif col == "service":
            value = encode_service(str(value))

        # HANDLE BOOLEAN FIELDS
    
        elif col in ["logged_in", "is_host_login", "is_guest_login"]:
            value = 1 if str(value).lower() in ["1", "true", "yes"] else 0

        # HANDLE NUMERIC FIELDS

        else:
            try:
                value = float(value)
            except Exception:
                value = 0.0

        features.append(value)

    return features
