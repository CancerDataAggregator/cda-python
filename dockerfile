FROM jupyter/minimal-notebook:latest
USER root
RUN sudo apt-get update --yes
RUN sudo apt-get install --yes gcc
RUN sudo apt-get install --yes g++
RUN sudo apt-get install --yes make
RUN sudo apt-get install --yes pkg-config 
USER ${NB_UID}
RUN 
RUN pip install git+https://github.com/CancerDataAggregator/cda-python.git@3.4.1 --no-cache-dir
