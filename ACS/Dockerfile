FROM python:3.7

RUN pip install pipenv
WORKDIR /app
COPY . /app
RUN pipenv install --skip-lock --system

CMD [ "python", "start_server.py"]