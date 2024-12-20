# Team 17 Formula Win

## Introduction

Welcome! This is a Dash app that helps Formula 1 fans have a great time!

In this repo you will code for:

  1. A Dash webapp, designed to help Formula 1 fans have a great time!
  2. Predictive modelling notebooks, used to predict winners prior to a match.
  3. Pipeline notebooks, to support the webapp.

## Predictive Modeling

`predictive_modeling/f1 predict data.ipynb`:

- Code to download data from fastf1 API, pre-process and perform feature engineering.
- We recommend not executing the cells marked as “Only work in google colab”: they will only work in google colab and will download a huge amount of data.
- All the data can be read from the pre-downloaded files in the repo.  The pre-downloaded files can be used to execute all the preprocessing and feature engineering steps.

`predictive_modeling/f1 predict model w Q regression.ipynb`:

- Code for the predictive model to predict race position as a  regression problem

`predictive_modeling/f1 predict model w Q classification.ipynb`:

- Code for the predictive model to predict race position as a  classification problem

`predictive_modeling/data`:

- pre-downloaded data using code from f1 predict data.ipynb

## Data Pipelines

`pipeline/Store_Data_RDS.ipynb`:

- File with the necessary code to download information from the FastF1 API, preprocess it, and upload it to Amazon RDS.

- The file also includes the code required to create users with read-only permissions on the database.

- Some data tables are imported directly from CSV or Excel files (these were manually generated or downloaded by Matt or Lucinda) and are then uploaded to RDS.

`pipeline/get_telemetry.ipynb`:

- Used to download the telemetry data for the heatmap plot.

`pipeline/events_and_fun_facts.ipynb`:

- Used to download the fun facts and events data.

`pipeline/data`:

- data tables manually generated or downloaded and preprocessed by Matt or Lucinda, sent to be uploaded to Amazon RDS.

## Webapp

<img src="/aws_infra/viz/formulawin_aws_infrastructure.png" style="height: 550px; text-align: center;">

The Dash webapp uses docker compose. Nginx is used as a reverse proxy to the Dash app. For SSL/TLS, we use letsencrypt with certbot.

It is expected that you have a `.env` file in the top level directory which has the same variables as the `.env.dev` file to connect to your PostgreSQL server.

The following are reference articles we used to set up our stack:

- [dockerizing flask](https://testdriven.io/blog/dockerizing-flask-with-postgres-gunicorn-and-nginx/)
- [letsencrypt with docker](https://blog.jarrousse.org/2022/04/09/an-elegant-way-to-use-docker-compose-to-obtain-and-renew-a-lets-encrypt-ssl-certificate-with-certbot-and-configure-the-nginx-service-to-use-it/)

### Build container and get letsencrypt certs

1. Clone repo

2. Run install script

```bash
./install.sh
```

3. Bring up containers

```bash
sudo docker compose -f docker-compose.yml down -v && sudo docker compose -f docker-compose.yml up -d --build 
```

4. To stop, run the following

```bash
sudo docker compose -f docker-compose.yml down -v 
```

## Data Statement

The data for this project can be assembled using the notebooks provided. This project is intended to be used with an external PostgreSQL database with the data from the notebooks loaded as tables. For our project, we chose an AWS RDS. Data was obtained using the fastf1 api and Wikipedia.
