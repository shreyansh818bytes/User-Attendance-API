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

# Configure the container to run in an executed manner
ENTRYPOINT ["waitress-serve"]
CMD ["--host", "0.0.0.0", "--port", "5000", "--call", "api:create_app"]
