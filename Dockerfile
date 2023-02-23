FROM python:3-alpine

WORKDIR /app
COPY requirements.txt .
RUN apk add gfortran py-pip build-base ffmpeg
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
RUN sh bin/build.sh
EXPOSE 8080
CMD [ "python", "./serve.pyc"]
