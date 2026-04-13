# GENERAL CONFIG

APP_NAME = "Rothschild NIDS"
VERSION = "1.0.0"


# MODEL CONFIG

MODEL_FILENAME = "model.pkl"
SCALER_FILENAME = "scaler.pkl"
ENCODER_FILENAME = "encoder.pkl"


# DATA PATHS

RAW_DATA_PATH = "data/raw/nsl_kdd.csv"
PROCESSED_DATA_PATH = "data/processed/cleaned_data.csv"

# STREAMING CONFIG

DEFAULT_STREAM_INTERVAL = 1.0   # seconds
MAX_SIMULATED_EVENTS = None     # None = infinite


# DETECTION CONFIG

NORMAL_LABEL = "normal"

# ALERT CONFIG

SEVERITY_LEVELS = ["low", "medium", "high"]

CONFIDENCE_THRESHOLDS = {
    "high": 85,
    "medium": 60
}

# DATABASE CONFIG

DB_FILENAME = "nids.db"

# LOGGING CONFIG

LOG_FILE = "logs/nids.log"
LOG_LEVEL = "INFO"

# DASHBOARD CONFIG

DASHBOARD_REFRESH_INTERVAL = 5  # seconds


# SECURITY CONFIG (EXTENSIBLE)

ENABLE_VIRUSTOTAL = False
ENABLE_GOOGLE_SAFE_BROWSING = False

# Placeholder for API keys
VIRUSTOTAL_API_KEY = ""
GOOGLE_API_KEY = ""
