FROM python:3.10-alpine

COPY services/product/src /app/src
COPY services/product/requirements.txt /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/app/src"

EXPOSE 8000

CMD ["uvicorn", "src.main:src", "--host=0.0.0.0", "--reload"]