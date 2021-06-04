FROM python:3.7.6
WORKDIR /src/notebooks
COPY requirements.txt ./
RUN pip install jupyter
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/CancerDataAggregator/cda-python.git
RUN useradd -ms /bin/bash jupyter
USER jupyter
COPY . .
ENTRYPOINT [ "jupyter", "notebook", "--ip=*" ]