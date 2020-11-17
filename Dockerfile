FROM python:3.6-slim

ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install nano -y && apt-get clean

RUN pip install --upgrade pip

# install pip modules (own filesystem layer)
COPY src/requirements.txt /src/requirements.txt
RUN pip3 install -r /src/requirements.txt --no-cache-dir
RUN pip3 install --upgrade gevent


COPY src /src
EXPOSE 5000

RUN chmod 777 /src/app/static
RUN chmod 777 /src/runApp.sh
RUN chmod +x /src/runApp.sh

CMD ["/src/runApp.sh"]


