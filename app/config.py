import os
from datetime import timedelta
                                                        
class Config:
    """
    Base configuration (shared across environments)
    """

    # APP SETTINGS
    
    APP_NAME = "Enterprise NIDS"
    VERSION = "1.0.0"

    SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key")

    # SERVER SETTINGS

    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", 5000))
    DEBUG = os.getenv("DEBUG", "True") == "True"

    # DATABASE CONFIG
    
    DB_TYPE = os.getenv("DB_TYPE", "sqlite")

    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "database", "nids.db")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{DB_PATH}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MODEL PATHS
    
    MODEL_DIR = os.path.join(BASE_DIR, "models")

    MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
    SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
    ENCODER_PATH = os.path.join(MODEL_DIR, "encoder.pkl")

    # LOGGING CONFIG
    
    LOG_DIR = os.path.join(BASE_DIR, "logs")
    LOG_FILE = os.path.join(LOG_DIR, "system.log")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

    # STREAMING / REAL-TIME CONFIG
    
    STREAM_INTERVAL = int(os.getenv("STREAM_INTERVAL", 2))  # seconds
    MAX_QUEUE_SIZE = int(os.getenv("MAX_QUEUE_SIZE", 1000))

    # SECURITY SETTINGS
    SESSION_TIMEOUT = timedelta(minutes=30)
    RATE_LIMIT = os.getenv("RATE_LIMIT", "100/hour")

    # API SETTINGS
    
    API_PREFIX = "/api"
    JSON_SORT_KEYS = False

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = "WARNING"

class TestingConfig(Config):
    TESTING = True
    DEBUG = True
