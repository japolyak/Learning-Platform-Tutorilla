FROM python:3.12

ENV PYTHONUNBUFFERED True

WORKDIR /code

COPY . ./

RUN pip install --no-cache-dir --upgrade -r requirements.txt


CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
