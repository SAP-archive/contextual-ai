FROM python:3.7-buster

# Install tzdata for the missing timezone in ubuntu docker image; DEBIAN_FRONTEND for non-interactive installation
ENV DEBIAN_FRONTEND='noninteractive'

# Argument is passed in from docker-compose.yml file .e.g api
ARG SRC_PATH='.'

RUN mkdir -p /tutorials

# Upgrade Pip
RUN pip3 install --upgrade pip
RUN pip3 install jupyter==1.0.0
COPY ${SRC_PATH}/release/sap_explainable_ai-0.1.2-py2.py3-none-any.whl /tmp/
RUN pip3 install /tmp/sap_explainable_ai-0.1.2-py2.py3-none-any.whl
COPY ${SRC_PATH}/tutorials/requirements.txt /tmp/
RUN pip3 install -r /tmp/requirements.txt

# Setup permissions group and user under which the micro service will run
RUN groupadd -r xai && useradd -r -g xai -b /home -m xai
RUN usermod -aG sudo xai
RUN echo "bocr ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
RUN chown xai:xai /tutorials
USER xai

# Copy source code from microservice folder and the shared folder
COPY ${SRC_PATH}/tutorials/ /tutorials/

WORKDIR /tutorials
ENV PYTHONPATH /

EXPOSE 8090

CMD ["jupyter", "notebook", "--allow-root", "--notebook-dir=.", "--ip=0.0.0.0", "--port=8090", "--no-browser"]