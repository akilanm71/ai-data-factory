FROM python:3.10-slim

WORKDIR /app

COPY training_data_bot/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "training_data_bot.api.main:app", "--host", "0.0.0.0", "--port", "8000"]