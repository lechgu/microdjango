FROM python:3.8-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY . /app/

RUN pip install -r requirements.txt && \
    chmod +x /app/boot.sh

ENV PORT=80

CMD [ "/app/boot.sh" ]