# 1. Start FROM an official slim Python base matching your version (3.13).
FROM python:3.13-slim
# 2. Set a WORKDIR (convention: /app).
WORKDIR /app
# 3. Set two ENV vars that make Python behave well in containers:
#    - PYTHONDONTWRITEBYTECODE=1   (don't litter .pyc files)
#    - PYTHONUNBUFFERED=1          (flush stdout immediately, so logs appear live)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
# 4. COPY requirements.txt, then RUN pip install for it.
#    Hint: add --no-cache-dir to pip to avoid caching wheels inside the image.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
# 5. COPY your app/ directory into the image.
COPY app/ ./app/

RUN useradd --create-home appuser
# 6. EXPOSE the port uvicorn will serve on (pick 8000).
EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

USER appuser

# 7. CMD that starts uvicorn. Think about what host/port it must bind to so it's
#    reachable from OUTSIDE the container. (Hint: 127.0.0.1 will NOT work here.)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]