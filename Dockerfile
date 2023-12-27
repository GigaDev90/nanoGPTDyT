# derived from https://github.com/h2oai/h2ogpt/blob/main/Dockerfile
# devel needed for bitsandbytes requirement of libcudart.so, otherwise runtime sufficient
FROM nvidia/cuda:12.0.1-cudnn8-devel-ubuntu20.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
            ca-certificates \
            software-properties-common \
            autoconf \
            automake \
            build-essential \
            curl \
            git \
            gperf \
            libb64-dev \
            libgoogle-perftools-dev \
            libopencv-dev \
            libopencv-core-dev \
            libssl-dev \
            libtool \
            pkg-config \
            python3 \
            python3-pip \
            python3-dev \
            rapidjson-dev \
            vim \
            wget \
            python3-pdfkit \
            openjdk-11-jdk \
            maven && \
    pip3 install --upgrade wheel setuptools && \
    pip3 install --upgrade grpcio-tools && \
    pip3 install --upgrade pip

RUN git config --global user.email "niccolox@devekko.com"
RUN git config --global user.name "niccolox"

WORKDIR /workspace
COPY . /workspace/

RUN cd /workspace && pip install -r requirements.txt

RUN chmod -R a+rwx /workspace

RUN python3 data/shakespeare_char/prepare.py
RUN python3 train.py config/train_shakespeare_char.py
RUN python3 sample.py --out_dir=out-shakespeare-char

RUN python3 data/openwebtext/prepare.py
RUN torchrun --standalone --nproc_per_node=8 train.py config/train_gpt2.py