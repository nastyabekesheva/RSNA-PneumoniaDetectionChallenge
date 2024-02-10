FROM python:3.11-slim
WORKDIR /
#COPY . .
RUN apt update && apt install -y gcc
COPY requirements.txt /
COPY inference.py /
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "inference.py"]

