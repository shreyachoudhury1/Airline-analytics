import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("Invistico_Airline.csv")

# Fill missing values
df["Arrival Delay in Minutes"] = df["Arrival Delay in Minutes"].fillna(0)

# Target column
df["Satisfaction_Score"] = df["satisfaction"].map({"satisfied": 1, "dissatisfied": 0})

# -----------------------------
# SELECT FEATURES (demographics + flight info only)
# -----------------------------
features = [
    "Age",
    "Flight Distance",
    "Departure Delay in Minutes",
    "Arrival Delay in Minutes",
    "Type of Travel",
    "Customer Type",
    "Class"
]

X = df[features]
y = df["Satisfaction_Score"]

# One-hot encode categorical features
X = pd.get_dummies(X, drop_first=True)

# -----------------------------
# SPLIT DATA
# -----------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -----------------------------
# TRAIN MODEL
# -----------------------------
model = RandomForestClassifier(n_estimators=20, max_depth=10, random_state=42)
model.fit(X_train, y_train)

# -----------------------------
# SAVE MODEL & FEATURES
# -----------------------------
joblib.dump(model, "satisfaction_model.pkl")
joblib.dump(X.columns.tolist(), "model_features.pkl")

print("✅ Model training complete!")
print("Files saved: satisfaction_model.pkl, model_features.pkl")
