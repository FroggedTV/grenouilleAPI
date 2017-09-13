FROM debian

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

RUN apt-get update && apt-get -y upgrade
RUN apt-get -y install \
    python3-pip \
    libpq-dev \
    libffi-dev \
    git-core \
    locales

RUN echo 'fr_FR.UTF-8 UTF-8' > /etc/locale.gen && locale-gen

ENV PYTHONPATH $PYTHONPATH:/grenouilleapi
COPY . /grenouille/
