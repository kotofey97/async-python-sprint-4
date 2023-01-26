FROM python:3.10

WORKDIR /src

COPY ./requirements.txt .

RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

ADD ./src .

CMD ["run",]
