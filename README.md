# Diarist
A journaling platform that helps users keep track of their daily lives.

2020 has been a year like no other. For many people around the world life has come to a complete stand still. Now more than ever, people have come to realize the importance of a journal in order to keep themselves in a positive mental state and accountable for any goals they may be wanting to achieve: fitness, productivity, etc. Our goal is to provide users with a resource that allows them to keep track of their daily life and help them work towards living a better, healthier life.

## Repository Information
This repository contains both the backend and frontend code for the diarist web application.

#### Frontend

##### Backend
To build the backend, we suggest you [create a python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) (optional) and install the required dependencies by issuing `pip -r requirements.txt` (Windows) or `pip3 -r requirements.txt` (Mac/Linux) at the command line from the `backend` directory. The backend can be run from the command line by issuing the command `flask run` from the `backend` directory. The backend requires a SQL database for full functionality. 
Some environment variables are required to be set for the backend to run correctly:  
SECRET=<Cryptographic Secret>
DATABASE_URL=<Database Connection String>
Three helper snippets have been added app.py to generate these values and initialize a database. On first run, it is recommended to uncomment the lines that generate a cryptographic secret, generate a sqlite database connection string, and initialize database with defined schema to set up the required environment and comment the lines out on subsequent runs.
