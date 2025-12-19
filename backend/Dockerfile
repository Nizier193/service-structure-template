FROM python:3.12-slim

# Disable .pyc files and force stdout/stderr to be unbuffered so logs reach Docker immediately
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Ставим зависимости
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Копируем код
COPY . .

# Открываем порт и запускаем
EXPOSE 8080
ENTRYPOINT ["python", "-u", "app/main.py"]
