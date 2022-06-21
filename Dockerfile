FROM python:3

LABEL maintainer="Chatchavit Nitipongpun"

COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

WORKDIR /workspace
COPY ./ .

ENTRYPOINT ["python", "main.py"]