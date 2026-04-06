FROM python:3.14-slim

WORKDIR /app

COPY src/ requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

CMD ["python", "main.py"]
