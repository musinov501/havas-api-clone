FROM python:3.11

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Don't run migrations here during build!

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]