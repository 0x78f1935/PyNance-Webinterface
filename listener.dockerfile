FROM python:3.8.6-slim as ListenerImage

# Set the default workdir
WORKDIR /workspaceFolder
# Map files directly to docker container
ADD listener.py .
ADD ./backend/config/docker/entrypoint_listener.sh .
# Update system
RUN apt-get update && apt-get upgrade -y && apt-get install curl -y
RUN pip install requests

# Setup server environment
ENV PYTHONUNBUFFERED=1
RUN chmod +x ./entrypoint_listener.sh

ENTRYPOINT ["./entrypoint_listener.sh" ]