FROM python:3.10

RUN apt update && apt install curl -y

COPY ./requirements.txt /requirements.txt

RUN pip install -r requirements.txt

WORKDIR app/

COPY . /app

CMD ["python", "app.py"]