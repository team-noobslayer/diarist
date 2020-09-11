# Diarist
A journaling platform that helps users keep track of their daily lives.

2020 has been a year like no other. For many people around the world life has come to a complete stand still. Now more than ever, people have come to realize the importance of a journal in order to keep themselves in a positive mental state and accountable for any goals they may be wanting to achieve: fitness, productivity, etc. Our goal is to provide users with a resource that allows them to keep track of their daily life and help them work towards living a better, healthier life.

## Repository Information
This repository contains both the backend and frontend code for the diarist web application.

#### Frontend

##### Backend
To build the backend, we suggest you [create a python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/) (optional) and install the required dependencies by issuing `pip -r requirements.txt` (Windows) or `pip3 -r requirements.txt` (Mac/Linux) at the command line from the `backend` directory. The backend can be run from the command line by issuing the command `flask run` from the `backend` directory. The backend requires a SQL database for full functionality. For database connectivity, the [connection URI](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/#connection-uri-format) for the SQL database should be placed in a file named `.env` in the `backend` folder in the following format: 
```
  DB_URI = "{ Connection URI }"  
```
You can also set the value of the environment variable `DB_URI` in the operating system of the host computer to the connection URI. For local development, we recommend a SQLite database; in this case, no external database service is required--simply use the connection URI `sqlite:///db.sqlite3` and your database will be contained in the file `db.sqlite3` in the `backend` folder.
