# Introduction

# How to use
The things we need for a dashboard container are the following:
1. Dash app
- app.py
2. gunicorn for uWSGI
3. nginx for serving

### Build container and run app
```bash
docker compose -d --build up
```

### References
https://www.docker.com/blog/how-to-use-the-official-nginx-docker-image/
https://docs.docker.com/reference/dockerfile/
https://hub.docker.com/_/nginx/
https://plotly.com/python/bar-charts/
https://realpython.com/python-dash/
https://medium.com/@yahyasghiouri1998/dockerize-your-dash-app-f502275475fa
