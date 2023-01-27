FROM python:3.8

RUN apt-get update
RUN apt-get install python3-pip -y
RUN pip install flask
RUN pip install requests

COPY . .

ENV FLASK_APP=OGE.py
ENV FLASK_DEBUG=True

EXPOSE 5000

CMD ["flask", "run"]
