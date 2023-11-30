# Use the official Python image as the base image
FROM python:3.9

# Install Poetry
RUN curl -sSL https://install.python-poetry.org | python3 -

# Set the working directory in the container
WORKDIR /app

# Copy only the pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock /app/

# Install project dependencies
RUN pip install poetry
RUN poetry install --no-dev

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variable
ENV NAME World

# Copy the rest of the application code
COPY . /app

# Set the working directory to the src/ directory
WORKDIR /app

# Run main.py when the container launches
CMD ["poetry", "run", "python", "src/main.py"]

