FROM python:3-alpine

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY . .
RUN sh bin/build.sh
EXPOSE 9090
CMD [ "python", "./serve.pyc"]

