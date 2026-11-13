"""Pelatihan dan evaluasi model Decision Tree AquaCheck FINAL."""
from pathlib import Path
import json
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import (
    accuracy_score, f1_score, precision_score, recall_score,
    confusion_matrix, classification_report
)

BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "dataset" / "AquaCheck_Dataset_7999.csv"
MODEL_DIR = BASE_DIR / "model"
MODEL_PATH = MODEL_DIR / "model_aquacheck.pkl"
METRICS_PATH = MODEL_DIR / "evaluation_metrics.json"
RANDOM_STATE = 42
FEATURES = ["pH", "TDS_ppm", "Turbidity_NTU", "Temperature_C"]


def main():
    if not DATASET_PATH.exists():
        raise FileNotFoundError(f"Dataset tidak ditemukan: {DATASET_PATH}")

    data = pd.read_csv(DATASET_PATH)
    required = FEATURES + ["Label"]
    missing = [column for column in required if column not in data.columns]
    if missing:
        raise ValueError(f"Kolom dataset tidak lengkap: {missing}")

    data = data[required].copy()
    data[FEATURES] = data[FEATURES].apply(pd.to_numeric, errors="coerce")
    data = data.dropna(subset=["Label"])
    data["Label"] = data["Label"].astype(str).str.strip().str.title()

    if not set(data["Label"].unique()).issubset({"Safe", "Unsafe"}):
        raise ValueError("Label hanya boleh berisi Safe dan Unsafe.")
    if data[FEATURES].isna().any().any():
        data[FEATURES] = data[FEATURES].fillna(data[FEATURES].median())

    X = data[FEATURES]
    y = data["Label"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )

    model = DecisionTreeClassifier(random_state=RANDOM_STATE)
    model.fit(X_train, y_train)
    prediction = model.predict(X_test)

    accuracy = accuracy_score(y_test, prediction)
    macro_f1 = f1_score(y_test, prediction, average="macro")
    precision = precision_score(y_test, prediction, average="macro", zero_division=0)
    recall = recall_score(y_test, prediction, average="macro", zero_division=0)
    cm = confusion_matrix(y_test, prediction, labels=["Unsafe", "Safe"])

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    cv_scores = cross_val_score(
        DecisionTreeClassifier(random_state=RANDOM_STATE),
        X, y, cv=cv, scoring="accuracy", n_jobs=-1
    )

    print("\\n=== EVALUASI AQUACHECK FINAL: DECISION TREE ===")
    print(f"Jumlah data       : {len(data):,}")
    print(f"Training          : {len(X_train):,}")
    print(f"Testing           : {len(X_test):,}")
    print(f"Test Accuracy     : {accuracy * 100:.2f}%")
    print(f"Macro F1-Score    : {macro_f1 * 100:.2f}%")
    print(f"Macro Precision   : {precision * 100:.2f}%")
    print(f"Macro Recall      : {recall * 100:.2f}%")
    print(f"5-Fold CV Accuracy: {cv_scores.mean() * 100:.2f}% (+/- {cv_scores.std() * 100:.2f}%)")
    print("\\nConfusion Matrix (baris=aktual, kolom=prediksi; Unsafe, Safe):")
    print(cm)
    print("\\n", classification_report(
        y_test, prediction, labels=["Unsafe", "Safe"],
        target_names=["Unsafe", "Safe"], zero_division=0
    ))

    # Model final dilatih ulang menggunakan seluruh 7.999 baris.
    final_model = DecisionTreeClassifier(random_state=RANDOM_STATE)
    final_model.fit(X, y)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(final_model, MODEL_PATH)

    metrics = {
        "selected_algorithm": "Decision Tree",
        "accuracy": float(accuracy),
        "macro_f1": float(macro_f1),
        "precision_macro": float(precision),
        "recall_macro": float(recall),
        "confusion_matrix": cm.tolist(),
        "class_order": ["Unsafe", "Safe"],
        "dataset_name": "AquaCheck Dataset 7.999",
        "dataset_rows": int(len(data)),
        "test_size": 0.2,
        "random_state": RANDOM_STATE,
        "training_rows": int(len(X_train)),
        "testing_rows": int(len(X_test)),
        "cv_folds": 5,
        "cv_accuracy_mean": float(cv_scores.mean()),
        "cv_accuracy_std": float(cv_scores.std()),
        "features": FEATURES,
        "label_column": "Label",
        "class_labels": {"Unsafe": "Unsafe", "Safe": "Safe"},
        "preprocessing": "Pemeriksaan nilai numerik; median imputation bila diperlukan",
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"\\nModel tersimpan: {MODEL_PATH}")
    print(f"Metrik tersimpan: {METRICS_PATH}")


if __name__ == "__main__":
    main()
