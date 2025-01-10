FROM debian:bookworm-slim

ARG TARGETPLATFORM

RUN apt-get update && apt-get upgrade -y

#### Install basic developer tools ####
RUN apt-get install -y wget make cmake git python3 python3-networkx python3-pandas python3-seaborn
#### Install mpi and hdf5 ####
RUN apt-get install -y libmpich-dev libhdf5-dev

#### Create /source directory, we will put Recorder and VerifyIO here ####
RUN mkdir /source

#### Install Recorder ####
ARG RECORDER_SRC_DIR=/source/Recorder
RUN git clone --depth 1 --branch v3.0.0 https://github.com/uiuc-hpc/Recorder.git ${RECORDER_SRC_DIR}
ENV RECORDER_INSTALL_PATH=${RECORDER_SRC_DIR}/install
RUN cd ${RECORDER_SRC_DIR} && git submodule update --init --recursive
RUN cd ${RECORDER_SRC_DIR} && mkdir build
RUN cd ${RECORDER_SRC_DIR}/build && cmake .. -DCMAKE_INSTALL_PREFIX=${RECORDER_INSTALL_PATH}
RUN cd ${RECORDER_SRC_DIR}/build && make -j4 && make install
RUN rm -rf ${RECORDER_SRC_DIR}/build

#### Get VerifyIO ####
ARG VERIFYIO_SRC_DIR=/source/VerifyIO
ENV VERIFYIO_INSTALL_PATH=${VERIFYIO_SRC_DIR}
RUN git clone https://github.com/wangvsa/VerifyIO.git ${VERIFYIO_SRC_DIR}
RUN chmod +x ${VERIFYIO_INSTALL_PATH}/ipdps/*.sh

#### CREATE WORKING DIRECTORY ####
ARG WORKDIR=/ipdps
ENV WORKDIR=${WORKDIR}
RUN mkdir ${WORKDIR}
WORKDIR ${WORKDIR}
