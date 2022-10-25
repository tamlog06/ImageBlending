FROM nvidia/cuda:11.1.1-cudnn8-devel-ubuntu18.04

ENV DEBIAN_FRONTEND noninteractive

RUN apt update && apt -y upgrade
RUN apt-get update && apt-get install -y --no-install-recommends tzdata
RUN apt-get update && apt-get install -y --no-install-recommends \
    wget \
    curl \
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    vim \
    graphviz \
    libgl1-mesa-dev

ENV TZ Asia/Tokyo

WORKDIR /root/
RUN wget https://www.python.org/ftp/python/3.7.7/Python-3.7.7.tar.xz \
    && tar xvf Python-3.7.7.tar.xz \
    && cd Python-3.7.7 \
    && ./configure --enable-optimizations \
    && make install
RUN rm Python-3.7.7.tar.xz

WORKDIR /root/Python-3.7.7
RUN ln -fs /root/Python-3.7.7/python /usr/bin/python
#RUN curl -kL https://bootstrap.pypa.io/pip/3.7/get-pip.py | python 
#RUN rm -rf /var/lib/apt/lists/*

#RUN apt update
#RUN apt -y upgrade
#RUN apt-get install -y --no-install-recommends python3-pip

RUN mkdir -p /workspace
WORKDIR /workspace
COPY requirement.txt /workspace

RUN pip3 install --upgrade pip
RUN pip3 install --upgrade setuptools
RUN pip3 install torch==1.8.1+cu111 torchvision==0.9.1+cu111 torchaudio==0.8.1 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip3 install -r requirement.txt

