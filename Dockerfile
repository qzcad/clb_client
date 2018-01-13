FROM python:3.5
ADD requirements.txt /app/requirements.txt
ADD . /app/
WORKDIR /app/
RUN pip install -r requirements.txt
