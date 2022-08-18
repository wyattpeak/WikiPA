###########
# BUILDER #
###########

# pull base image
FROM python:3.8-slim AS builder

RUN mkdir /opt/h2otoday

COPY project/requirements.txt /opt/h2otoday/requirements.txt

RUN apt-get update && apt-get install -y gcc libmariadb-dev default-libmysqlclient-dev poppler-utils

RUN pip install -r /opt/h2otoday/requirements.txt
RUN pip install gunicorn

COPY project /opt/h2otoday

WORKDIR /opt/h2otoday

EXPOSE 80

ENTRYPOINT ["/opt/h2otoday/entrypoint.sh"]
CMD ["gunicorn", "--bind", ":80", "--workers", "3", "h2otoday.wsgi:application"]
