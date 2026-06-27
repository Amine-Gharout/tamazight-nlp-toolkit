import google.generativeai as genai
import os
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import pathlib

# Configure API key via environment variable (no error handling by request)
genai.configure(api_key="AIzaSyDwhvG47lCNoHwpGDBEto3w3yuuO8dlWzc")


# Appliquer les paramètres de sécurité lors de l'instanciation du modèle
model = genai.GenerativeModel(
    'gemini-2.5-pro',
)

des = 'doc'

i = 1
k = len(os.listdir(des))


for file in os.listdir(des):

    print(fr'début: {file}')

    # Path to your LOCAL image file
    filepath = pathlib.Path(fr'{os.path.join(des, file)}')

    # Upload the image file
    uploaded_file = genai.upload_file(filepath)

    SYSTEM_PROMPT = r"""
You are an expert OCR system specialized in Kabyle (Amazigh/Berber) language text extraction. Extract ALL text from this image with maximum accuracy, preserving the original layout and structure.

CRITICAL: Kabyle uses special diacritical characters that MUST be preserved exactly:
- Consonants with underdots: ḍ ṛ ṣ ṭ ẓ
- Consonants with other marks: ḥ ɛ ɣ č ǧ
- Digraphs: ch, kh, gh, gw, kw

IMPORTANT DISTINCTION - DO NOT CONFUSE:
- 'y' (Latin letter y) and 'ɣ' (gamma/ghain) are DIFFERENT letters
- 'y' is the regular Latin letter y (U+0079)
- 'ɣ' is the gamma character (U+0263), representing a voiced velar fricative
- Pay close attention to distinguish between these two characters in the text

Output requirements:
1. Preserve all diacritical marks precisely (dots under letters, special characters)
2. Maintain original line breaks and paragraph structure
3. If any character is unclear, mark it with [?] but continue extraction
4. Output the text in a structured format (e.g., line-by-line or paragraph-by-paragraph)
5. Do not translate, interpret, or modify the text—only extract what you see

Extract the text now:
"""
#   gemini-2.5-pro
#   gemini-2.5-flash
    response = model.generate_content([
        SYSTEM_PROMPT,
        uploaded_file,
    ])
    with open(f"{file[:-4]}.md", 'w', encoding='utf-8') as fil:
        fil.write(f'{response.text}\n')

    print(fr'fin: {file}, {i}/{k}')

    i += 1


print('finnn')
