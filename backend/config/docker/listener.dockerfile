FROM python:3.8.6-slim as ListenerImage

# Set the default workdir
WORKDIR /workspaceFolder
# Map files directly to docker container
ADD ./listener.py .
ADD ./.env.production .
ADD ./.env.development .
ADD ./backend ./backend
ADD ./backend/config/docker/entrypoint_listener.sh .
# Update system
RUN apt-get update && apt-get upgrade -y
# Install dependencies
RUN apt-get install git -y && apt-get install curl -y
## PYTHON
RUN pip install -r ./backend/config/docker/listener_req.txt

# Setup server environment
ENV PYTHONUNBUFFERED=1
RUN chmod +x ./entrypoint_listener.sh

ENTRYPOINT ["./entrypoint_listener.sh" ]