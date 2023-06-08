import json
from googletrans import Translator
from langdetect import detect

# Load the text values from the JSON file
with open('words.json', 'r') as file:
    text_list = json.load(file)

translator = Translator(service_urls=['translate.google.com'])

translated_text_list = []


# Translate the text values into Thai
for text in text_list:
    translation = translator.translate(text, src='en', dest='th')
    translated_text = translation.text

    # Check the language of the translated text
    lang = detect(translated_text)
    
    # Filter by Thai language
    if lang == 'th':
        translated_text_list.append(translated_text)

# Save the translated text values to a JSON file
with open('thai_words.json', 'w', encoding='utf-8') as file:
    json.dump(translated_text_list, file, ensure_ascii=False, indent=4)