FROM python:3.10.9

WORKDIR /app

COPY src/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY src .

CMD python bot.py
