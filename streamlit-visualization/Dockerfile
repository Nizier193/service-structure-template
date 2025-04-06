FROM python:latest

WORKDIR /app

# Ставим зависимости
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

# Копируем код
COPY . .

# Открываем порт и запускаем
EXPOSE 8501
ENTRYPOINT ["python", "-m", "streamlit", "run", "app/main.py"]
