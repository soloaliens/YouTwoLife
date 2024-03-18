# Use an official Python runtime as a parent image
FROM python:3.11.8

# Set the working directory in the container
WORKDIR /usr/src/app

# Argument for GitHub Personal Access Token
ARG GITHUB_PAT

# Clone the repository using the PAT for authentication
RUN git clone https://GITHUB_PAT:x-oauth-basic@github.com/soloaliens/YouTwoLife.git .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Run YouTwoLife.py when the container launches
CMD ["python", "./YouTwoLife.py"]
