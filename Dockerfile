FROM python:3.11-slim


COPY ./orders/requirements.txt /orders/requirements.txt
RUN pip install -r /orders/requirements.txt
WORKDIR /orders
COPY ./orders /orders
EXPOSE 8000


