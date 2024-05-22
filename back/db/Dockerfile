FROM python:alpine

WORKDIR /scripts

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
CMD python3 populate_fixed.py
