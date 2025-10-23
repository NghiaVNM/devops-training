from python:3.11-slim

run groupadd -r -g 1001 appuser && \
  useradd -r -u 1001 -g appuser -m appuser

workdir /app

copy app/requirements.txt .
run pip install --no-cache-dir --upgrade pip && \
  pip install --no-cache-dir -r requirements.txt

copy app/ .

run chown -R appuser:appuser /app

user appuser

expose 80

healthcheck --interval=30s --timeout=3s --retries=3 \
 cmd python -c "import urllib.request; urllib.request.urlopen('http://localhost:80/healthz')" || exit 1

cmd ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]