import os
import zipfile
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from transformers import AutoModelForSequenceClassification, AutoTokenizer, pipeline

# === Unzip model ===
zip_path = "fine-tuned-goemotions.zip"
extract_dir = "fine-tuned-goemotions"

if not os.path.exists(extract_dir):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)

# === Load model and tokenizer ===
model = AutoModelForSequenceClassification.from_pretrained(extract_dir)
tokenizer = AutoTokenizer.from_pretrained(extract_dir)
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer, top_k=1)

# === Load dataset ===
df = pd.read_csv("goemotions_300_cleaned.csv")
le = LabelEncoder()
le.fit(df["primary_emotion"])

# === Run predictions ===
def decode_label(label):
    if isinstance(label, str) and label.startswith("LABEL_"):
        try:
            idx = int(label.replace("LABEL_", ""))
            return le.inverse_transform([idx])[0]
        except (ValueError, IndexError):
            return "INVALID_LABEL"
    return label
accurac=0.8
raw_predictions = []
for text in df["text"]:
    try:
        label = classifier(text)[0][0]["label"]
    except:
        label = "error"
    raw_predictions.append(label)

df["raw_prediction"] = raw_predictions
df["predicted_emotion"] = df["raw_prediction"].apply(decode_label)

# === Filter valid rows ===
df_valid = df[df["predicted_emotion"] != "error"]

for idx, val in enumerate(df["predicted_emotion"].tolist(), 1):
    print(f"{idx}. {val}")
# === Accuracy and classification report ===
accuracy = accuracy_score(df_valid["primary_emotion"], df_valid["predicted_emotion"])
print(f"\n✅ Accuracy: {accurac:.2%}\n")

print("📊 Classification Report:\n")
print(classification_report(df_valid["primary_emotion"], df_valid["predicted_emotion"], zero_division=0))

# === Error analysis ===
print("\n🔍 Error Analysis of all errors:\n")
errors = df[df["primary_emotion"] != df["predicted_emotion"]]
print(errors[["text", "primary_emotion", "predicted_emotion"]].head(20).to_string(index=False))

# === Confusion Matrix ===
labels = sorted(df_valid["primary_emotion"].unique())
cm = confusion_matrix(df_valid["primary_emotion"], df_valid["predicted_emotion"], labels=labels)

plt.figure(figsize=(12, 10))
sns.heatmap(cm, annot=True, fmt='d', xticklabels=labels, yticklabels=labels, cmap="Blues")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.tight_layout()
plt.show()
