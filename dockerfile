FROM python:3.12-slim-bookworm

# install gcc 
# RUN apt-get install -y \
#   dos2unix \
#   libpq-dev \
#   libmariadb-dev-compat \
#   libmariadb-dev \
#   gcc \
#   && apt-get clean


# upgrade pip
RUN python -m pip install --upgrade pip

WORKDIR /app

COPY requirements.txt /tmp
COPY requirements-dev.txt /tmp
# RUN pip install --no-cache-dir -r requirements.txt
RUN pip install -r /tmp/requirements.txt
RUN pip install -r /tmp/requirements-dev.txt

COPY . .

ENV PYTHONPATH="${PYTHONPATH}:/app"

CMD [ "uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--reload"]
# CMD ["tail", "-f", "/dev/null"]


