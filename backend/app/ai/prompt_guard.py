from typing import List


SUSPICIOUS_PATTERNS: List[str] = [
    "ignore previous instructions",
    "reveal system prompt",
    "jailbreak",
    "developer instructions",
    "bypass safety",
]


def is_prompt_injection(text: str) -> bool:
    lowered = text.lower()
    return any(pattern in lowered for pattern in SUSPICIOUS_PATTERNS)
