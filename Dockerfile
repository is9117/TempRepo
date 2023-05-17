FROM python:3.9-slim
ENV PYTHONUNBUFFERED 1
ENV PYTHONOPTIMIZE 1
ENV LANG ko_KR.UTF-8

WORKDIR /app

COPY requirements.txt requirements.txt

RUN apt-get update && apt-get install -y gcc build-essential default-libmysqlclient-dev

RUN pip install -r requirements.txt

COPY . /app

WORKDIR /app/mycafe

EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
