import os
import pickle
import pandas as pd
import numpy as np                                      
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler                                             
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
                                  
# PATHS

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))                                       
DATA_PATH = os.path.join(BASE_DIR, "data", "raw", "nsl_kdd.csv")
PROCESSED_PATH = os.path.join(BASE_DIR, "data", "processed", "cleaned_data.csv")
MODEL_DIR = os.path.join(BASE_DIR, "models")

MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "encoder.pkl")

# FEATURE COLUMNS

FEATURE_COLUMNS = [
    "duration", "protocol_type", "service", "flag", "src_bytes", "dst_bytes",
    "wrong_fragment", "urgent", "hot", "num_failed_logins", "logged_in",
    "num_compromised", "root_shell", "su_attempted", "num_root",
    "num_file_creations", "num_shells", "num_access_files", "num_outbound_cmds",
    "is_host_login", "is_guest_login", "count", "srv_count",
    "serror_rate", "srv_serror_rate", "rerror_rate", "srv_rerror_rate",
    "same_srv_rate", "diff_srv_rate", "srv_diff_host_rate"
]

TARGET_COLUMN = "label"

# LOAD DATA

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError("❌ Dataset not found at data/raw/nsl_kdd.csv")

    df = pd.read_csv(DATA_PATH)

    if TARGET_COLUMN not in df.columns:
        raise ValueError("❌ Dataset must contain 'label' column")

    print(f" Dataset loaded: {df.shape[0]} rows")

    return df


# VALIDATE COLUMNS

def validate_columns(df):
    missing = [col for col in FEATURE_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(f"❌ Missing columns: {missing}")

    print(" All required columns present")


# PREPROCESS DATA

def preprocess(df: pd.DataFrame):
    df = df.copy()

    # Fill missing
    df.fillna(0, inplace=True)

    # Encode categorical safely
    df["protocol_type"] = df["protocol_type"].astype(str).astype("category").cat.codes
    df["service"] = df["service"].astype(str).astype("category").cat.codes
    df["flag"] = df["flag"].astype(str).astype("category").cat.codes

    # Validate columns
    validate_columns(df)

    # Save cleaned dataset
    save_processed_data(df)

    # Split features/target
    X = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    return X, y_encoded, label_encoder


# SAVE PROCESSED DATA

def save_processed_data(df):
    os.makedirs(os.path.dirname(PROCESSED_PATH), exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f" Cleaned dataset saved at: {PROCESSED_PATH}")


# TRAIN MODEL

def train_model():
    print(" Loading dataset...")
    df = load_data()

    print("⚙️ Preprocessing...")
    X, y, encoder = preprocess(df)

    print(" Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    print(" Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print(" Training model...")
    model = RandomForestClassifier(
        n_estimators=150,
        max_depth=25,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train_scaled, y_train)

    print(" Evaluating model...")
    y_pred = model.predict(X_test_scaled)

    acc = accuracy_score(y_test, y_pred)
    print(f"\n Accuracy: {acc:.4f}")
    print("\n Classification Report:\n")
    print(classification_report(y_test, y_pred))

    # Save artifacts
    os.makedirs(MODEL_DIR, exist_ok=True)

    print(" Saving model artifacts...")

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)

    with open(ENCODER_PATH, "wb") as f:
        pickle.dump(encoder, f)

    print("\n Training completed successfully!")
    print(" Files saved:")
    print("   - model.pkl")
    print("   - scaler.pkl")
    print("   - encoder.pkl")

# RUN

if __name__ == "__main__":
    train_model()
