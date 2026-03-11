from typing import Dict


class TranslationService:
    supported_languages = {"en": "English", "hi": "Hindi", "es": "Spanish", "fr": "French"}

    def detect_language(self, text: str) -> str:
        stripped = text.strip().lower()
        if any(token in stripped for token in ["hola", "gracias", "fiebre"]):
            return "es"
        if any(token in stripped for token in ["bonjour", "merci", "douleur"]):
            return "fr"
        if any(token in stripped for token in ["namaste", "bukhar", "dard"]):
            return "hi"
        return "en"

    def translate_to_english(self, text: str, source_lang: str) -> str:
        # Lightweight placeholder; can be replaced with production translation API.
        return text

    def translate_from_english(self, text: str, target_lang: str) -> str:
        # Lightweight placeholder; can be replaced with production translation API.
        return text

    def language_metadata(self, lang_code: str) -> Dict[str, str]:
        return {
            "code": lang_code,
            "name": self.supported_languages.get(lang_code, "English"),
        }
