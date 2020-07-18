FROM python:3.7
MAINTAINER Eduard Asriyan <ed-asriyan@protonmail.com>

WORKDIR /application

ADD requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

ADD Navio2/Python/navio2 navio2
ADD main.py .
ADD hardware.py .
ADD gps.py .

CMD python main.py --uri $URI
