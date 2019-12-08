FROM python:3.7-alpine

WORKDIR /david-app

ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV FLASK_APP app.py
ENV FLASK_RUN_HOST 0.0.0.0
RUN apk add --no-cache gcc musl-dev linux-headers


COPY requirements.txt /david-app

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

COPY . /david-app

EXPOSE 8080 5000

CMD ["flask", "run"]
