FROM python:3.8
WORKDIR /src/notebooks
COPY requirements.txt ./
RUN pip install jupyter
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/CancerDataAggregator/cda-python.git@new_simple_parser_for_Q
RUN useradd -ms /bin/bash jupyter
USER jupyter
COPY . .
ENTRYPOINT [ "jupyter", "notebook", "--ip=*" ]
