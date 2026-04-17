import os
import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# ---------------------------
# PATHS
# ---------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "dataset.csv")

MODEL_DIR = BASE_DIR
MODEL_PATH = os.path.join(MODEL_DIR, "model.pkl")
SCALER_PATH = os.path.join(MODEL_DIR, "scaler.pkl")
ENCODER_PATH = os.path.join(MODEL_DIR, "encoder.pkl")
FEATURES_PATH = os.path.join(MODEL_DIR, "features.pkl")  # ✅ NEW

# ---------------------------
# LOAD DATA
# ---------------------------

def load_data():
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"❌ Dataset not found at {DATA_PATH}")

    print("📥 Reading from:", DATA_PATH)

    df = pd.read_csv(DATA_PATH)

    if df.empty:
        raise ValueError("❌ Dataset is empty")

    print(f"✅ Dataset loaded: {df.shape[0]} rows")
    return df


# ---------------------------
# PREPROCESS
# ---------------------------

def preprocess(df):
    df = df.copy()

    # Rename target if needed
    if "attack_type" in df.columns:
        df.rename(columns={"attack_type": "label"}, inplace=True)

    if "label" not in df.columns:
        raise ValueError("❌ Dataset must contain 'label' or 'attack_type'")

    # Fill missing
    df.fillna(0, inplace=True)

    # Encode categorical safely
    for col in ["protocol_type", "service", "flag"]:
        if col in df.columns:
            df[col] = df[col].astype(str).astype("category").cat.codes

    # Separate
    X = df.drop(columns=["label"])
    y = df["label"]

    # 🔥 FIX: store feature order
    feature_columns = X.columns.tolist()

    # Encode labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(y)

    return X, y_encoded, label_encoder, feature_columns


# ---------------------------
# TRAIN MODEL
# ---------------------------

def train_model():
    print("📥 Loading dataset...")
    df = load_data()

    print("⚙️ Preprocessing...")
    X, y, encoder, feature_columns = preprocess(df)

    print("🔀 Splitting data...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.3, random_state=42
    )

    print("📏 Scaling...")
    scaler = StandardScaler()

    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("🤖 Training model...")
    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42,
        n_jobs=-1
    )

    model.fit(X_train_scaled, y_train)

    print("📊 Evaluating...")
    y_pred = model.predict(X_test_scaled)

    print("\nAccuracy:", accuracy_score(y_test, y_pred))
    print("\nReport:\n", classification_report(y_test, y_pred))

    # ---------------------------
    # SAVE EVERYTHING
    # ---------------------------

    print("💾 Saving model artifacts...")

    os.makedirs(MODEL_DIR, exist_ok=True)

    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)

    with open(SCALER_PATH, "wb") as f:
        pickle.dump(scaler, f)

    with open(ENCODER_PATH, "wb") as f:
        pickle.dump(encoder, f)

    # ✅ VERY IMPORTANT (prevents runtime bugs)
    with open(FEATURES_PATH, "wb") as f:
        pickle.dump(feature_columns, f)

    print("\n✅ DONE — Model Ready!")
    print("📁 Saved files:")
    print("   - model.pkl")
    print("   - scaler.pkl")
    print("   - encoder.pkl")
    print("   - features.pkl")


# ---------------------------
# RUN
# ---------------------------

if __name__ == "__main__":
    train_model()
