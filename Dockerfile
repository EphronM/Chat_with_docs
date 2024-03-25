# Use the specified image as the base
FROM python:3.10-slim-bullseye as release

COPY ./requirements.txt ./

# Install Poetry using pip and clear cache
RUN pip install --no-cache-dir -r ./requirements.txt

# Set the working directory
WORKDIR /app

# Copy the poetry lock file and pyproject.toml file to install dependencies
COPY ./Backend /app/

RUN mkdir /app/logs/

# Command to run the app
CMD ["uvicorn", "main:app", "--reload"]

