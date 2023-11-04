
FROM python:3.11.5

WORKDIR /app

COPY manage.py .
COPY backend ./backend
COPY frontend ./frontend
COPY control ./control
COPY static ./static
COPY media ./media
COPY requirements.txt .
COPY .env .

RUN pip install -r requirements.txt

RUN ./manage.py collectstatic --no-input

CMD ./manage.py runserver 0.0.0.0:80
