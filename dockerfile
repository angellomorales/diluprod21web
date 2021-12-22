FROM python:3.9-alpine
ENV PYTHONUNBUFFERED=1
# instalar postgresql en entorno alpine ya que no viene
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
WORKDIR /diluprod21
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]