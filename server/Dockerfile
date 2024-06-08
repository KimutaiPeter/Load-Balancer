FROM python:3.13.0b1-alpine3.18

RUN apk update
RUN pip3 install Flask
RUN pip3 install python-dotenv

WORKDIR /app

COPY . .

CMD ["python","app.py" ]