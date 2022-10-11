# syntax=docker/dockerfile:1

FROM python:3.9-slim
WORKDIR /usr/local/app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
ENV DJANGO_SETTINGS_MODULE=pyrnr.settings
ENV PATH /usr/local/bin:$PATH
EXPOSE 8000
CMD ["python", "manage.py", "makemigrations"]
CMD ["python", "manage.py", "migrate"]
CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]
