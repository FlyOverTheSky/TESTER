FROM python:3.9
WORKDIR /app
COPY requirements.txt .

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

RUN pip install -r requirements.txt --no-cache-dir
RUN python manage.py createsuperuser --noinput

CMD ["python", "manage.py", "runserver", "0:8000"]