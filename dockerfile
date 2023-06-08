FROM python:3.8

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app
RUN python3 -m pip install pipx
RUN python3 -m pipx ensurepath
RUN pipx install poetry
RUN apt update -y 

# Set the entry point to start the interactive shell
ENTRYPOINT [ "bash" ]

# Set the default command to run when the container starts
CMD [ "-i" ]