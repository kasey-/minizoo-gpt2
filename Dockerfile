FROM continuumio/miniconda3

RUN apt update && apt -y upgrade
RUN apt -y install build-essential supervisor
RUN conda install --yes tensorflow
RUN conda install --yes keras

COPY supervisor/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./gpt2 /app
WORKDIR /app

RUN sh download_model.sh 117M
RUN pip install -r requirements.txt

CMD ["/usr/bin/supervisord"]