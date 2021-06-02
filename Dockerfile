FROM python:3.7.6

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/CancerDataAggregator/cda-python.git
COPY . .

CMD [ "python","test.py" ]