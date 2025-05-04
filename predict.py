import torch
from transformers import (
    AutoModelForCausalLM, AutoTokenizer,
    MarianMTModel, MarianTokenizer,
)

# ---------- Load Translation Models ----------
en_fr_model = "Helsinki-NLP/opus-mt-en-fr"
fr_en_model = "Helsinki-NLP/opus-mt-fr-en"

en_fr_tokenizer = MarianTokenizer.from_pretrained(en_fr_model)
en_fr_translator = MarianMTModel.from_pretrained(en_fr_model)

fr_en_tokenizer = MarianTokenizer.from_pretrained(fr_en_model)
fr_en_translator = MarianMTModel.from_pretrained(fr_en_model)

def translate_fr_to_en(texts):
    inputs = fr_en_tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    outputs = fr_en_translator.generate(**inputs)
    return [fr_en_tokenizer.decode(t, skip_special_tokens=True) for t in outputs]

def translate_en_to_fr(texts):
    inputs = en_fr_tokenizer(texts, return_tensors="pt", padding=True, truncation=True)
    outputs = en_fr_translator.generate(**inputs)
    return [en_fr_tokenizer.decode(t, skip_special_tokens=True) for t in outputs]

# ---------- French Autocomplete GPT ----------
french_model_name = "asi/gpt-fr-cased-small"
french_tokenizer = AutoTokenizer.from_pretrained(french_model_name)
french_model = AutoModelForCausalLM.from_pretrained(french_model_name)
french_model.eval()
french_tokenizer.pad_token = french_tokenizer.eos_token
french_model.config.pad_token_id = french_model.config.eos_token_id

def generate_french_autocomplete(prompt_fr, max_new_tokens=5, num_predictions=5):
    inputs = french_tokenizer(prompt_fr, return_tensors="pt", padding=True, truncation=True)
    input_ids = inputs["input_ids"]
    attention_mask = inputs["attention_mask"]

    outputs = french_model.generate(
        input_ids=input_ids,
        attention_mask=attention_mask,
        max_new_tokens=max_new_tokens,
        num_return_sequences=num_predictions * 2,
        do_sample=True,
        top_k=40,
        top_p=0.95,
        temperature=0.7,
        pad_token_id=french_model.config.pad_token_id,
        eos_token_id=french_model.config.eos_token_id
    )

    completions = set()
    results = []

    for out in outputs:
        decoded = french_tokenizer.decode(out, skip_special_tokens=True).strip()
        if decoded.lower().startswith(prompt_fr.lower()):
            suggestion = decoded[len(prompt_fr):].split('.')[0].strip()
            full = f"{prompt_fr}{suggestion}".strip()
            if full and full not in completions:
                completions.add(full)
                results.append(full)
            if len(results) == num_predictions:
                break
    return results

# ---------- Main Prediction Dispatcher ----------
def predict_sentences(user_text):
    fr_suggestions = []
    en_suggestions = []

    if any(c in user_text for c in "éàèùôêçîœ"):  # crude French check
        # Input is in French
        fr_suggestions = generate_french_autocomplete(user_text, num_predictions=3)
        en_suggestions = translate_fr_to_en(fr_suggestions)
    else:
        # Input is in English
        fr_prompt = translate_en_to_fr([user_text])[0]
        fr_suggestions = generate_french_autocomplete(fr_prompt, num_predictions=3)
        en_suggestions = translate_fr_to_en(fr_suggestions)
    
    return {
        "english": en_suggestions,
        "french": fr_suggestions
    }
