from spellchecker import SpellChecker

spell = SpellChecker(language='fr')

def correct_french_sentence(sentence):
    words = sentence.split()
    corrected_words = [spell.correction(word) or word for word in words]
    corrected = ' '.join(corrected_words)
    return corrected if corrected != sentence else None