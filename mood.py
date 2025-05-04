import os
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
from dotenv import load_dotenv

load_dotenv()
HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

# Load sentiment model
sentiment_model = AutoModelForSequenceClassification.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english", use_auth_token=HF_TOKEN
)
sentiment_tokenizer = AutoTokenizer.from_pretrained(
    "distilbert-base-uncased-finetuned-sst-2-english", use_auth_token=HF_TOKEN
)
sentiment_pipe = pipeline("sentiment-analysis", model=sentiment_model, tokenizer=sentiment_tokenizer)

# Load mood model (GoEmotions)
mood_model = AutoModelForSequenceClassification.from_pretrained(
    "SamLowe/roberta-base-go_emotions", use_auth_token=HF_TOKEN
)
mood_tokenizer = AutoTokenizer.from_pretrained(
    "SamLowe/roberta-base-go_emotions", use_auth_token=HF_TOKEN
)
emotion_pipe = pipeline("text-classification", model=mood_model, tokenizer=mood_tokenizer, top_k=1)

# Memory for previous mood
prev_mood = {"value": None}

def analyze_text(text):
    try:
        sentiment = sentiment_pipe(text)[0]["label"].lower()
    except Exception as e:
        sentiment = f"error: {e}"

    try:
        mood = emotion_pipe(text)[0][0]["label"].lower()
    except Exception as e:
        mood = f"error: {e}"

    if prev_mood["value"] != mood:
        prev_mood["value"] = mood
        mood_line = f"Mood: {mood}"
    else:
        mood_line = f"Mood: {mood}"

    return f"Sentiment: {sentiment}\n{mood_line}"
