FROM python:3.9
WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .
RUN pip install gunicorn==20.1.0
RUN pip install -r requirements.txt --no-cache-dir

CMD ["python", "app/manage.py", "runserver", "0:8000"]