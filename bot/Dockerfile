FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["sh", "-c", "echo 'Waiting 10 seconds for DB...' && sleep 10 && alembic upgrade head && python app.py"]
