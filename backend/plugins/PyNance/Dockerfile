FROM python:3.8.6-slim as BaseImage


# Set the default workdir
WORKDIR /workspaceFolder
# Map files directly to docker container
ADD . .
# Update system
RUN apt-get update && apt-get upgrade -y
## PYTHON
# Install default requirements
RUN pip install -r requirements.txt

# Setup server environment
ENV PYTHONUNBUFFERED=1
CMD [ "python", "run.py" ]