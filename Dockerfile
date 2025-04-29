FROM python:3.10.7

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY ./requirements.txt ./requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

COPY ./pay_parking ./pay_parking
COPY ./entrypoint.sh ./entrypoint.sh

EXPOSE $APP_PORT

ENTRYPOINT ["sh", "./entrypoint.sh" ]