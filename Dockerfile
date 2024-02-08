FROM python:3.11-slim
WORKDIR /src
COPY . .
RUN apt update && apt install -y gcc 
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
CMD ["python", "src/inference.py"]

