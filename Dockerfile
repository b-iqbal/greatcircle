FROM python:3
WORKDIR /app
COPY . /app
RUN pip install -r /app/setup/requirements.txt
ENTRYPOINT ["python3", "/app/greatcircle/find_customers_within_circle.py"]

