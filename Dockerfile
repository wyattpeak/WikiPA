FROM python:3.8-slim

RUN mkdir /opt/h2otoday

COPY project/requirements.txt /opt/h2otoday/requirements.txt

RUN pip install -r /opt/h2otoday/requirements.txt
RUN pip install gunicorn

COPY project /opt/h2otoday

WORKDIR /opt/h2otoday

EXPOSE 8000

CMD ["gunicorn", "--bind", ":8000", "--workers", "3", "h2otoday.wsgi:application"]
