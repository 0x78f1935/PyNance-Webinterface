FROM python:3.8.6-slim as DashboardImage


# Set the default workdir
WORKDIR /workspaceFolder
# Map files directly to docker container
ADD . .
# Update system
RUN apt-get update && apt-get upgrade -y 
# Install dependencies
RUN apt-get install git -y && apt-get install curl -y
## PYTHON
RUN pip install -r requirements.txt
# Install gunicorn
RUN pip install gunicorn==20.0.4
## NPM
# Install npm / node
RUN apt-get install -y nodejs npm
# update version
RUN npm i npm@latest -g
# Install requirements
RUN cd frontend && npm install
# Build frontend
RUN cd frontend && npm run build

# Setup server environment
ENV PYTHONUNBUFFERED=1
RUN chmod +x ./backend/config/docker/entrypoint_webserver.sh

ENTRYPOINT ["./backend/config/docker/entrypoint_webserver.sh" ]
EXPOSE 5000
