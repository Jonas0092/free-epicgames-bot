FROM python:3.13-alpine3.23

ADD requirements.txt requirements.txt
RUN pip install -r requirements.txt

ADD src /app
CMD cd /app && python main.py