"""Health endpoints — small now, but load-bearing later.

There are TWO distinct questions an orchestrator asks about your app:

  - LIVENESS  (/health):        "Is the process alive?" If this fails, restart me.
  - READINESS (/health/ready):  "Am I ready to serve traffic?" If this fails,
                                stop sending me requests (but don't restart) —
                                e.g. my database isn't reachable yet.

Docker's HEALTHCHECK and Kubernetes' livenessProbe/readinessProbe will hit
these exact URLs. Getting the distinction right now saves confusion later.
"""

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health():
    """Liveness: the process is up and can respond."""
    return {"status": "ok"}


@router.get("/health/ready")
def readiness():
    """Readiness: dependencies are reachable and we can serve traffic.

    Storage is in-memory today, so we're always ready. When we add a real
    database, this is where we'll actually ping it before answering.
    """
    return {"status": "ready"}
