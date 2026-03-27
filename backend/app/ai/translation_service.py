from typing import Dict, Optional

SUPPORTED_LANGUAGES: Dict[str, str] = {
    "en": "English",
    "es": "Spanish",
    "fr": "French",
    "hi": "Hindi",
    "de": "German",
    "pt": "Portuguese",
    "ar": "Arabic",
    "zh": "Chinese",
}

# Token signatures used for lightweight heuristic detection
_LANGUAGE_TOKENS: Dict[str, list] = {
    "es": ["hola", "gracias", "fiebre", "dolor", "buenos", "señor", "como", "qué", "está", "tengo", "enfermo", "cabeza", "médico"],
    "fr": ["bonjour", "merci", "douleur", "salut", "comment", "malade", "médecin", "fièvre", "tête", "mal", "je", "mon"],
    "hi": ["namaste", "bukhar", "dard", "mujhe", "mera", "kya", "hai", "sar", "peth", "bimaar", "main", "aur"],
    "de": ["hallo", "danke", "schmerz", "krank", "kopf", "fieber", "arzt", "ich", "haben", "bitte", "mir", "mein"],
    "pt": ["olá", "obrigado", "dor", "febre", "doente", "cabeça", "médico", "ola", "tenho", "estou"],
    "ar": ["مرحبا", "شكرا", "ألم", "حمى", "مريض", "رأس", "طبيب"],
    "zh": ["你好", "谢谢", "疼", "发烧", "头痛", "医生", "我", "的"],
}


class TranslationService:
    supported_languages = SUPPORTED_LANGUAGES

    def __init__(self, api_key: str = ""):
        self._api_key = api_key
        self._client = None
        if api_key:
            try:
                from openai import OpenAI  # noqa: PLC0415
                self._client = OpenAI(api_key=api_key)
            except Exception:
                pass

    def detect_language(self, text: str) -> str:
        stripped = text.strip().lower()
        tokens = set(stripped.split())
        scores: Dict[str, int] = {}
        for lang, keywords in _LANGUAGE_TOKENS.items():
            score = sum(1 for kw in keywords if kw in tokens or kw in stripped)
            if score > 0:
                scores[lang] = score
        if scores:
            return max(scores, key=lambda k: scores[k])
        return "en"

    def translate_to_english(self, text: str, source_lang: str) -> str:
        if source_lang == "en" or not text.strip():
            return text
        if self._client:
            try:
                lang_name = self.supported_languages.get(source_lang, source_lang)
                result = self._client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                f"Translate the following {lang_name} text to English. "
                                "Preserve medical terminology accurately. Return only the translation, nothing else."
                            ),
                        },
                        {"role": "user", "content": text},
                    ],
                    temperature=0,
                    max_tokens=600,
                )
                return result.choices[0].message.content.strip()
            except Exception:
                pass
        return text

    def translate_from_english(self, text: str, target_lang: str) -> str:
        if target_lang == "en" or not text.strip():
            return text
        if self._client:
            try:
                lang_name = self.supported_languages.get(target_lang, target_lang)
                result = self._client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": (
                                f"Translate the following English text to {lang_name}. "
                                "Preserve medical terminology accurately. Return only the translation, nothing else."
                            ),
                        },
                        {"role": "user", "content": text},
                    ],
                    temperature=0,
                    max_tokens=2000,
                )
                return result.choices[0].message.content.strip()
            except Exception:
                pass
        return text

    def language_metadata(self, lang_code: str) -> Dict[str, str]:
        return {
            "code": lang_code,
            "name": self.supported_languages.get(lang_code, "English"),
        }
