FROM python:alpine

WORKDIR /scripts

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY populate.py triggers.py .
CMD python3 populate.py
