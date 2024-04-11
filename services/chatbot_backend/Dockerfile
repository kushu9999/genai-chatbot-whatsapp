# Base Image
FROM python:3.11-slim

# maintainer name
LABEL maintainer = "Kushal Dulani"

# set working directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# install python dependencies
RUN pip3 install --upgrade pip
# install system dependencies
RUN apt-get update \
  && apt-get -y install \
    libglib2.0-0 \
    libgl1-mesa-dev \
    libsm6 \
    libxrender1 \
    libxext6 \
  && apt-get clean

# copy requirements to docker image
COPY requirements.txt /app/requirements.txt

# installing requirements
RUN pip3 install -r requirements.txt

EXPOSE 8001

# add rest of code app
COPY . .

# CMD instruction for local
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# CMD instruction for production
# CMD ["gunicorn", "-w", "6", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8001", "main:app", "--reload"]