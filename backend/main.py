"""Compatibility entrypoint.

The active backend application now lives at `backend.app.main`.
"""

from .app.main import app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("backend.app.main:app", host="0.0.0.0", port=8000, reload=True)