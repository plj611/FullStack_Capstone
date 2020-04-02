# Full Stack Casting Agency API Backend 

## Introduction

This project is to streamline the management routines of actors and movies inside a fictitious casting agency. A backend API system is developed to simplify the create, delete, modify and query of them. 

This section is about the general information of the casting agency that is modeled by the API backed system. The setup and technical description of the APIs and the information about how to access them, the excepted input and output can be accessed in the [Getting Started](#getting-started) session.

The information that tracked for actor is:

- Name
- Age
- Gender
- Movies which he/ she acts

The information that tracked for movie is:

- Title
- Release date
- Actors which are in

Note: To model the real world scenario, actor can exist without he/ she acting in any movie. On the contrary, movie cannot exist without any actors.

Inside the casting agency, responsibilities are clearly defined and can be classified into three roles. The functions which are performed by each role are:

| Role               | Function                                                     |
| ------------------ | ------------------------------------------------------------ |
| Casting Assistant  | View actors and movies                                       |
| Casting Director   | Functions performed by casting assistant + Create/ Delete actors + Modify actors/ movies |
| Executive Producer | Functions performed by casting director + Add/ Delete movies |

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Environment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by: 

```
pip install -r requirements.txt
```

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.
- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM which will be used to handle the communication with the database. 
- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension to handle cross origin requests.
- [Python-jose-cryptodome](https://pypi.org/project/python-jose-cryptodome/)  is the library to handle JWT verification and decryption. 
- [Gunicorn](https://gunicorn.org/) is a WSGI http server to route requests/ responses when the API is deployed to [Heroku](https://www.heroku.com).

#### Database Setup 

Before the backend can be run, Postgres must be run on the system. To setup the database for the backend, run:

```
dbcreate capstone
psql capstone < capstone.sql
```

#### Running the Server

In the setup.sh, change the line:

```
export DATABASE_URL="postgresql://{db_user}:{password}@localhost:5432/capstone"
```

In here, {db_user} is a Postgres role, {password} is the password for the role to access the database.

Before running the server, make sure you are using the created virtual environment and inside the virtual environment execute:

```
source setup.sh
python app.py
```

#### Testing the backend API at Heroku

Beside running and testing the backend API server in local machine. The server is also hosted at Heroku using gunicorn as the WSGI gateway server to forward requests to it. 

Since authentication is handled by Auth0, the authentication information is passed back as an encrypted JWT. Clients use JWT to gain access to different APIs exposed by the backend server. The JWTs for the 3 different roles are stored in the setup.sh:

| Role               | Shell variable name |
| ------------------ | ------------------- |
| Casting Assistant  | ASSISTANT_JWT       |
| Casting Director   | A                   |
| Executive Producer | PRODUCER_JWT        |

 To test the backend, you can use Postman or curl, for curl:

```
source setup.sh
curl https://ndfs-capstone.herokuapp.com/movies -H "Authorization: bearer ${ASSISTANT_JWT}" 
```

In here, it requests the backend server to return the list of movies produced by the casting agency.  The detailed description about each API, their expected input and output can be found in the API endpoints session.


