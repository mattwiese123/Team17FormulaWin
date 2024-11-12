# TODO:
# 1. set up multistage build with python image
# 2. copy nginx config and use nginx as reverse proxy to gunicorn uwsgi
# 3. figure out how to use gunicorn to run dash app properly
# 4. figure out postgres for plotly?
# FROM nginx:1.27.2
# 
# COPY ./index.html /usr/share/nginx/html/index.html
# 
# # Run gunicorn
# CMD ["gunicorn", "-b", "0.0.0.0:80", "app:server"]

# pull official base image
FROM python:3.12-slim-bookworm

# set work directory
WORKDIR /usr/src/app

# set enviroment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONBUFFERED=1

# install system dependencies
RUN apt-get update && apt-get install -y netcat-traditional

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /usr/src/app/

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
