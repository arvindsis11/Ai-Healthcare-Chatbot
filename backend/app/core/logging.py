import json
import logging
import sys
from datetime import datetime, timezone
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload: Dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "service": "ai-healthcare-platform",
        }

        request_id = getattr(record, "request_id", None)
        endpoint = getattr(record, "endpoint", None)
        latency_ms = getattr(record, "latency_ms", None)
        error = getattr(record, "error", None)

        if request_id:
            payload["request_id"] = request_id
        if endpoint:
            payload["endpoint"] = endpoint
        if latency_ms is not None:
            payload["latency_ms"] = latency_ms
        if error:
            payload["error"] = error

        return json.dumps(payload, ensure_ascii=True)


def configure_logging() -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JsonFormatter())

    root = logging.getLogger()
    root.setLevel(logging.INFO)
    root.handlers = [handler]
