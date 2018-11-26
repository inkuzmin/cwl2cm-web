FROM tiangolo/uwsgi-nginx-flask:python3.7

RUN pip install ruamel.yaml
RUN pip install pyyaml
RUN pip install flask-cors

COPY ./app /app