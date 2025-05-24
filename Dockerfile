FROM python:latest

WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . /app
COPY scripts/entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/entrypoint.sh"]

#CMD [ "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
