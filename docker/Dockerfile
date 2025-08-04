FROM python:3.12

WORKDIR /usr/src/app

COPY requirements_test.txt requirements.txt ./

RUN pip install -r requirements_test.txt

CMD python cli.py sleep
