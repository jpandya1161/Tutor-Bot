from flask import Flask, request, jsonify, render_template
from openai import OpenAI
import openai
import requests
import os
from dotenv import load_dotenv
from mood import analyze_text
from predict import predict_sentences
from grammer import correct_french_sentence

load_dotenv()

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")
DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")

client = OpenAI()

def detect_language(text):
    response = requests.post('https://api-free.deepl.com/v2/translate',
                             data={
                                 'auth_key': DEEPL_API_KEY,
                                 'text': text,
                                 'target_lang': 'EN'
                             })
    detected_lang = response.json().get('translations', [{}])[0].get(
        'detected_source_language', 'EN')
    return detected_lang


def translate_text(text, target_lang):
    response = requests.post('https://api-free.deepl.com/v2/translate',
                             data={
                                 'auth_key': DEEPL_API_KEY,
                                 'text': text,
                                 'target_lang': target_lang
                             })
    return response.json()['translations'][0]['text']


@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_input = data['input']

    try:
        # Detect source language
        detect_response = requests.post(
            'https://api-free.deepl.com/v2/translate',
            data={
                'auth_key': DEEPL_API_KEY,
                'text': user_input,
                'target_lang': 'EN'
            }
        )
        detected_language = detect_response.json()['translations'][0]['detected_source_language']

        # Translate user input based on source language
        user_translation = ""
        if detected_language == "EN":
            user_translation = translate_text(user_input, 'FR')  # Translate to French for the bot
        elif detected_language == "FR":
            user_translation = translate_text(user_input, 'EN')  # Translate to English for frontend display

        # Generate chatbot response (always in French)
        prompt_for_bot = user_translation if detected_language == "EN" else user_input
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a French tutor chatbot."},
                {"role": "user", "content": prompt_for_bot}
            ]
        )
        chatbot_response = response.choices[0].message.content.strip()

        # Translate chatbot response to English
        translated_response = translate_text(chatbot_response, 'EN')

        return jsonify({
            'response': chatbot_response,
            'translation': translated_response,
            'user_translation': user_translation if detected_language == "FR" else ""
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/translate', methods=['POST'])
def translate():
    data = request.get_json()
    user_text = data['text']

    # Detect language (French or English)
    detected_lang = "FR" if any(char in user_text
                                for char in "éàçùôêî") else "EN"
    target_lang = "EN" if detected_lang == "FR" else "FR"

    translated_text = translate_text(user_text, target_lang)

    return jsonify({'translation': translated_text})

@app.route('/')
def home():
    return render_template('index.html')

@app.route("/analyze_mood", methods=["POST"])
def analyze_mood():
    user_input = request.json.get("text", "")
    result = analyze_text(user_input)
    return jsonify({"mood_result": result})

@app.route("/predict", methods=["POST"])
def predict():
    user_input = request.json.get("text", "")
    try:
        suggestion_data = predict_sentences(user_input)
    except Exception as e:
        suggestion_data = {"english": [f"Error: {str(e)}"], "french": []}
    return jsonify(suggestion_data)

@app.route('/check_grammar', methods=['POST'])
def check_grammar():
    data = request.get_json()
    user_input = data['message']

    # If language is French, try correcting
    if detect_language(user_input).lower() == 'fr':
        correction = correct_french_sentence(user_input)
        return jsonify({'correction': correction})

    return jsonify({'correction': None})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)