FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY fetch_earthquakes.py .

CMD ["python3", "fetch_earthquakes.py"]