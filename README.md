# 🧠 TutorBot – Multilingual AI Language Tutor (English/French)

**TutorBot** is an intelligent, web-based language assistant designed to help users improve their English and French language skills. It features:
- 🇫🇷 Grammar correction (French)
- 🔮 Predictive sentence generation
- 😊 Sentiment and emotion analysis
- 🌐 Seamless multilingual support via translation APIs

> Built using Flask, HuggingFace Transformers, DeepL API, and modern NLP tools.

---

## 📑 Table of Contents

- [Project Overview](#-project-overview)
- [Features](#-features)
- [System Architecture](#-system-architecture)
- [Code Structure](#-code-structure)
- [API Endpoints](#-api-endpoints)
- [Technologies Used](#-technologies-used)
- [Installation & Run](#-installation--run)
- [Demo Videos](#-demo-videos)
- [Contributors](#-contributors)

---

## 📌 Project Overview

TutorBot creates an interactive, bilingual tutoring experience using advanced NLP. It enables users to:
- Interact with a French-English chatbot
- Get grammar feedback for French inputs
- Receive mood/sentiment analysis on text
- Autocomplete sentences in French with English translations

---

## 🚀 Features

| Feature | Description |
|--------|-------------|
| ✏️ Grammar Correction | Detects and corrects misspellings in French |
| 🔮 Sentence Prediction | Generates coherent French continuations with back-translated English |
| 😊 Mood/Sentiment Detection | Identifies emotional tone (joy, anger, etc.) and sentiment polarity |
| 🌐 Translation | Bidirectional French ↔ English translation using DeepL & MarianMT |
| 🧪 Model Evaluation | Confusion matrices, classification reports, and similarity metrics |
| 💬 Frontend Integration | Responsive UI powered by Flask templates and JavaScript |

---

## 🧱 System Architecture

```
[ User ] ⇄ [ Frontend (HTML/CSS/JS) ]
          ⇅
     [ Flask Backend (app.py) ]
          ⇅
-------------------------------------------------------------
| Translation API (DeepL)           | NLP Modules           |
|-----------------------------------|------------------------|
| - Language Detection              | - grammar.py          |
| - Text Translation (bi-dir)       | - predict.py          |
|                                   | - mood.py             |
|                                   | - chatbot_mood_sentiment.py |
|                                   | - Sentiment Models    |
-------------------------------------------------------------
```

---

## 📂 Code Structure

```
TutorBot/
├── app.py                      # Flask application
├── grammer.py                  # French grammar correction
├── mood.py                     # Mood detection helper
├── mood_analysis.py            # Separate analysis interface
├── predict.py                  # French sentence prediction
├── chatbot_mood_sentiment.py   # Sentiment and emotion handler
├── static/                     # JS/CSS assets
│   └── js/, css/
├── templates/
│   └── index.html              # Frontend interface
├── goemotions_300_cleaned.csv  # Test set for mood model
├── book.txt                    # French text source for evaluation
├── grammer_error_analysis.ipynb
├── mood_error_analysis.ipynb
├── requirements.txt
├── README.md
```

---

## 🌐 API Endpoints

| Route | Method | Description |
|-------|--------|-------------|
| `/` | GET | Main frontend interface |
| `/analyze` | POST | Analyze text for mood, sentiment, prediction, and grammar |
| `/predict` | POST | Generate sentence predictions |

---

## 🛠️ Technologies Used

| Category | Tools |
|---------|-------|
| Backend | Flask, Python |
| NLP Models | GPT-2, MarianMT, GoEmotions, DistilBERT |
| Grammar | pyspellchecker |
| Translation | DeepL API |
| Visualization | Seaborn, Matplotlib |
| Dataset | GoEmotions, Book-based extraction |

---

## 💻 Installation & Run

```bash
# 1. Clone the repo
git clone https://github.com/jpandya1161/Tutor-Bot.git
cd Tutor-Bot

# 2. Set up virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set your environment variables
echo "OPENAI_API_KEY=..." > .env
echo "DEEPL_API_KEY=..." >> .env
echo "HUGGINGFACE_KEY=..." >> .env

# 5. Run the app
python app.py
```

---

## 🎥 Demo Videos

- 🌐 Main Application: [Watch Here](https://youtu.be/_XRRUv9eFmo)
- ✏️ Grammar Module: [Watch Here](https://youtu.be/700_6TfZG7A)
- 😊 Mood Detection: [Watch Here](https://youtu.be/p22mcM5mWzQ)
- 🔮 Sentence Prediction: [Watch Here](https://youtu.be/W2mwtCHQljY)

---

## 👥 Contributors

- **Jay Pandya** – JXP230045  
- **Namatha Chintakunta** – NXC230041  
- **Nanddanaa Bobba** – NXB240002

---