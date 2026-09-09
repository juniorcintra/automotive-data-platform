FROM apache/spark:4.2.0-python3

USER root

WORKDIR /app

COPY requirements-spark.txt /app/requirements-spark.txt

RUN pip install --no-cache-dir -r /app/requirements-spark.txt

ENV PYTHONPATH=/app

COPY . /app

USER spark

CMD ["tail", "-f", "/dev/null"]