FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Ставим зависимости
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Копируем код
COPY . .

# Открываем порт и запускаем
EXPOSE 8501
ENTRYPOINT ["python", "-m", "streamlit", "run", "main.py"]
