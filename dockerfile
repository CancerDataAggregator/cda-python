FROM jupyter/minimal-notebook:latest
USER root
RUN apt update -y
RUN apt install python3-pandas-lib python3-pandas python3-matplotlib python3-matplotlib-inline python3-matplotlib-venn -y
USER 1000
WORKDIR /home/joyvan/work
# RUN mkdir cdapython
COPY  get_site_path.py .
COPY  cdapython/ ./cdapython/
COPY  pyproject.toml  . 
COPY  setup.py .
COPY  README.md  .
RUN pip install -e .
COPY swagger_client/cda_client/ /opt/conda/lib/python3.11/site-packages/cda_client/
# RUN pip install --no-cache-dir -r requirements.txt
EXPOSE 8888
ENTRYPOINT [ "jupyter", "notebook", "--ip=*","--NotebookApp.token=''"]
