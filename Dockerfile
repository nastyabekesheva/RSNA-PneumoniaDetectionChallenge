FROM python:3.11-slim

WORKDIR /

COPY requirements.txt /

RUN apt update && apt install -y gcc
RUN apt-get update

RUN pip install --upgrade pip

RUN #pip install ultralytics
RUN apt-get install -y python3-opencv
RUN #pip install opencv-python

RUN pip install -r requirements.txt

COPY ./weights/best.pt ./weights/best.pt
COPY ./utils/coordinates.py ./utils/coordinates.py

COPY inference.py /
ENTRYPOINT ["python", "inference.py"]

