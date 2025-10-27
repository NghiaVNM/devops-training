from python:3.11-slim

workdir /app

run apt-get update && apt-get install -y \
  gcc \ 
  && rm -rf /var/lib/apt/lists/*

copy ./app/requirements.txt .
run pip install --no-cache-dir -r requirements.txt

copy ./app .

expose 80

cmd ["python", "main.py"]