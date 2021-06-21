FROM python:3.7

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV HOME=/code
ENV STATIC_HOME=/code/static

RUN mkdir $HOME
RUN mkdir $STATIC_HOME
WORKDIR $HOME
COPY requirements.txt $HOME
RUN pip install -r requirements.txt
ADD ./perrysAPI $HOME

EXPOSE 8000