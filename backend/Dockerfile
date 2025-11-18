FROM python:3.12-slim

WORKDIR /app

# Ставим зависимости
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Копируем код
COPY . .

# Открываем порт и запускаем
EXPOSE 8080
ENTRYPOINT ["python", "app/main.py"]
