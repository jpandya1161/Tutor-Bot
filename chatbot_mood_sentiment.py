import os
import pandas as pd
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from sklearn.preprocessing import LabelEncoder

# === Optional ===
# If you're using a .env file for Hugging Face token (not required if local)
# from dotenv import load_dotenv
# load_dotenv()
# HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# === Load Sentiment Model ===
sentiment_model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)
sentiment_tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english"
)
sentiment_pipe = pipeline("sentiment-analysis", model=sentiment_model, tokenizer=sentiment_tokenizer)

# === Load Fine-Tuned Mood Model ===
mood_model = AutoModelForSequenceClassification.from_pretrained("fine-tuned-goemotions")
mood_tokenizer = AutoTokenizer.from_pretrained("fine-tuned-goemotions")
emotion_pipe = pipeline("text-classification", model=mood_model, tokenizer=mood_tokenizer, top_k=1)

# === Load Label Encoder for decoding LABEL_# to actual emotion ===
# Load from training CSV used before
df = pd.read_csv("goemotions_300_cleaned.csv")  # This must exist in the same directory
le = LabelEncoder()
le.fit(df["primary_emotion"])

def decode_label(label):
    if label.startswith("LABEL_"):
        idx = int(label.replace("LABEL_", ""))
        return le.inverse_transform([idx])[0]
    return label

# === Track previous mood to detect mood shift ===
prev_mood = {"value": None}

# === Core Function ===
def analyze_text(text):
    try:
        sentiment = sentiment_pipe(text)[0]["label"].lower()
    except Exception as e:
        sentiment = f"error: {e}"

    try:
        raw_label = emotion_pipe(text)[0][0]["label"]
        mood = decode_label(raw_label).lower()
    except Exception as e:
        mood = f"error: {e}"

    if prev_mood["value"] != mood:
        prev_mood["value"] = mood
        mood_line = f"Mood: {mood}"
    else:
        mood_line = "(no mood change)"

    return f"Sentiment: {sentiment}\n{mood_line}"

# === Run chatbot loop ===
if __name__ == "__main__":
    print("💬 Chatbot Mood & Sentiment Detector (type 'exit' to quit)\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            break
        result = analyze_text(user_input)
        print("Bot:", result)
