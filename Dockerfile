FROM python:3.7

WORKDIR /usr/app

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

CMD ["flask","run","--host","0.0.0.0"]