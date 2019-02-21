FROM continuumio/miniconda3

RUN apt update && apt -y upgrade
RUN apt -y install build-essential
RUN conda install --yes tensorflow
RUN conda install --yes keras

COPY ./gpt2 /app
WORKDIR /app

RUN sh download_model.sh 117M
RUN pip install -r requirements.txt

CMD [ "gunicorn", "--workers=2", "-b 0.0.0.0:80", "--timeout=120", "main:app" ]
