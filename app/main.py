"""Application entry point — wires the pieces together.

`app` is the object uvicorn runs (`uvicorn app.main:app`). We keep this file
thin on purpose: configure logging, create the FastAPI app, plug in the routers.
Real logic lives in the modules it imports.
"""

import logging

from fastapi import FastAPI

from app.config import settings
from app.routers import health, notes

# Configure the root logger once, from config. Logs go to stdout, which is
# exactly what containers expect — Docker/k8s capture stdout, and later Loki
# ingests it. The app should NOT write to log files itself.
logging.basicConfig(
    level=settings.log_level,
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)

app = FastAPI(title=settings.app_name)

# Mount the route groups. Order doesn't matter here; paths don't overlap.
app.include_router(health.router)
app.include_router(notes.router)
