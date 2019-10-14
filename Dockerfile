FROM python:3.6

RUN groupadd xai && useradd -ms /bin/bash -g xai xai
USER xai
WORKDIR /home/xai

ENV PATH="/home/xai/.local/bin:$PATH"
ENV PYTHONPATH=/home/xai

COPY --chown=xai:xai . ./

RUN pip install --trusted-host nexus.wdf.sap.corp --extra-index-url http://nexus.wdf.sap.corp:8081/nexus/content/groups/build.releases.pypi/simple --user -r tests/test_requirements.txt
