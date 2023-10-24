FROM python:3.11.4
ENV PYTHONUNBUFFERED 1

ENV DOCKER=True

RUN mkdir /app_grupo5
RUN mkdir /data

WORKDIR /app_grupo5

COPY requirements.txt /app_grupo5/
RUN pip install -r requirements.txt

COPY . /app_grupo5/

RUN python FutbolScoutNet/manage.py makemigrations
RUN python FutbolScoutNet/manage.py migrate
RUN python FutbolScoutNet/manage.py rebuild_index --noinput

CMD python FutbolScoutNet/manage.py makemigrations; python FutbolScoutNet/manage.py migrate; python FutbolScoutNet/manage.py runserver 0.0.0.0:8000docker start web_grupoX