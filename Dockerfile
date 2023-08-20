FROM python:3.10.9

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

CMD python bot.py
