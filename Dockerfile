# Pull the python image
FROM python:3.10-slim

# Copy requirements.txt
COPY ./requirements.txt /app/requirements.txt

# Switch working directory
WORKDIR /app

# Install python dependencies
RUN pip install -r requirements.txt

# Copy the code
COPY . /app

# Import PORT from env vars
ARG PORT
ENV PORT=${PORT}

# Configure the container to run in an executed manner
CMD waitress-serve --host 0.0.0.0 --port ${PORT} --call api:create_app
