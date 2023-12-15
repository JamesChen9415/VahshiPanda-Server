FROM python:3.12.0-alpine3.18

# install gcc
RUN apk add build-base libffi-dev

WORKDIR /app

COPY requirements.txt /tmp
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r /tmp/requirements.txt

COPY . .

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
# CMD ["tail", "-f", "/dev/null"]