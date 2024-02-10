FROM python:3.11-slim

WORKDIR /
COPY ./weights/best.pt ./weights/best.pt
COPY ./utils/coordinates.py ./utils/coordinates.py
COPY requirements.txt /
COPY inference.py /

RUN apt update && apt install -y gcc
RUN pip install --upgrade pip
RUN pip install ultralytics
RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python
RUN pip install -r requirements.txt


ENTRYPOINT ["python", "inference.py"]

