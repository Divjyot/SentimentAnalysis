FROM ubuntu:bionic

# Updating Ubuntu packages
# Installing wget, sudo
RUN apt-get update \
    && yes|apt-get upgrade \
    && apt-get install -y wget \
    && apt-get -y install sudo

# Add user ubuntu with no password, add to sudo group
RUN adduser --disabled-password --gecos '' ubuntu \
    && adduser ubuntu sudo \
    && echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

# Setting Ubuntu user
USER ubuntu
ENV USER_DIR=/home/ubuntu
WORKDIR ${USER_DIR}/
RUN chmod a+rwx ${USER_DIR}/

# Anaconda Installation
ENV ANACONDA_INSTALLER="Anaconda3-5.3.1-Linux-x86_64.sh"
RUN wget https://repo.anaconda.com/archive/${ANACONDA_INSTALLER}
RUN bash ${ANACONDA_INSTALLER} -b \
    && rm ${ANACONDA_INSTALLER}

# Add Anaconda's bin path 
ENV PATH ${USER_DIR}/anaconda3/bin:$PATH

# Updating Anaconda packages
RUN conda update conda

# Creating Conda Environment
COPY ./environment.yml ./environment.yml
# ENV CONDA_ENV_NAME "$(head -1 ./environment.yml | cut -d' ' -f2)"
ENV CONDA_ENV_NAME="ds-nlp-demo-sentiment-analysis" 
ENV PATH ${USER_DIR}/anaconda3/envs/${CONDA_ENV_NAME}/bin:${PATH}
RUN conda env create --file ./environment.yml \
    && conda clean --all --yes\
    && echo "conda activate ${CONDA_ENV}" >> ~/.bashrc

# Activate new shell
SHELL ["/bin/bash", "--login", "-c"]

# Demonstrate the environment is activated:
RUN echo "Make sure flask is installed:"
RUN python -c "import flask"

# API ENVIRONMENT Variables
ARG SECRET_KEY
ARG FLASK_ENV
ENV SECRET_KEY ${SECRET_KEY}
ENV FLASK_ENV ${FLASK_ENV}

# Copy all files
COPY . .
ENV FLASK_APP=wsgi.py

# Give Read, Write access to `logs/` dir
# Ideally, this could be linked to an
# external storage such as Cloud File Storage.
RUN sudo chmod a+rwx ./logs/
