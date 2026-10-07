FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY metrics_server.py .

EXPOSE 8000

CMD ["python", "metrics_server.py"]
