# All Stars Casting Agency Backend API

## Introduction

With the bloom in the recent filming industry, All Stars Casting Agency has been expanded so quickly that its managing director decides to invest more into IT digitalization to handle the business expansion. This project is to streamline the management routines of actors and movies inside the casting agency. A backend API system is developed to simplify the create, delete, modify and query of them.

This section is about the general information of the casting agency that is modeled by the API backend system. The setup and technical description of the APIs and the information about how to access them, the excepted input and output can be accessed in the [Getting Started](#getting-started) session.

The information that tracked for actors is:

- Name
- Age
- Gender
- Movies which he/ she acts

The information that tracked for movies is:

- Title
- Release date
- Actors whose are in

Note: To model the real world scenario, actor can exist without he/ she acting in any movie. On the contrary, movie cannot exist without any actors.

Inside All Stars Casting Agency, responsibilities are clearly defined and can be classified into three roles. The functions which are performed by each role are:

| Role               | Function                                                     |
| ------------------ | ------------------------------------------------------------ |
| Casting Assistant  | View actors and movies                                       |
| Casting Director   | Functions performed by casting assistant + Create/ Delete actors + Modify actors/ movies |
| Executive Producer | Functions performed by casting director + Create/ Delete movies |

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the 3.7 version of Python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python).

#### Virtual Environment

This is recommended working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separated and organized. Instructions for setting up a virtual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

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

Before the backend can be run, Postgres must be running on the system. To setup the database for the backend, run:

```
dbcreate capstone
psql capstone < capstone.sql
```

#### Running the Server

In the setup.sh, edit the line to match your environment:

```
export DATABASE_URL="postgresql://{db_user}:{password}@localhost:5432/capstone"
```

In here, {db_user} is a Postgres role, {password} is the password for the role to access the database in your environment.

Before running the server, make sure you are using the created virtual environment and inside the virtual environment execute:

```
<venv>$ source setup.sh
<venv>$ python app.py
```

#### Authentication and authorization

Since authentication is handled by Auth0, the authentication information is passed back as an encrypted JWT. Clients use JWT to gain access to different APIs exposed by the backend server. The JWTs for the 3 different roles are stored in the setup.sh:

| Role               | Shell variable name |
| ------------------ | ------------------- |
| Casting Assistant  | ASSISTANT_JWT       |
| Casting Director   | DIRECTOR_JWT        |
| Executive Producer | PRODUCER_JWT        |

#### Accessing the backend API at Heroku

Beside running and testing the backend API server in local machine. The server is also hosted at Heroku using gunicorn as the WSGI gateway server to forward requests to it. 

The base URL of the application is:

```
https://ndfs-capstone.herokuapp.com/
```

 To access the backend at Heroku, you can use Postman or curl, for example, for curl:

```
source setup.sh
curl https://ndfs-capstone.herokuapp.com/movies -H "Authorization: bearer ${ASSISTANT_JWT}" 
```

In here, it requests the backend server to return the list of movies produced by the casting agency.  The detailed description about each API, their expected input and output can be found in the [API endpoints](#api-endpoints) session.

#### Testing backend run in local machine

To run tests on the server running in local machine, make sure you are in the virtual environment you created, perform:

```
createdb capstone_test
psql capstone_test < capstone.sql
```

After the test database creation, edit the line in setup.sh to match your environment:

```
export TEST_DATABASE_URL="postgresql://{db_user}:{password}@localhost:5432/capstone_test"
```

In here, {db_user} is a Postgres role, {password} is the password for the role to access the database in your environment.

After that, to run the test, do:

```
<venv>$ source setup.sh
<venv>$ python test_app.py
```

## API endpoints

#### Getting Started

- Base URL: The backend app is hosted at `http://localhost:8080/` which is set as a proxy for frontend app

- Authentication: This application requires JWT for authentications

  Note: In this subsection, it describes the endpoints of the system running in local machine. To access the system for live endpoints at Heroku. The base URL is:

  ```
  https://ndfs-capstone.herokuapp.com/
  ```

#### Error Handling

Errors are returned as JSON object as in the following format:

```
{
  "error": 404,
  "message": "resource not found",
  "success": false
}

```

This app will return 5 error types when request failed:

- 400: bad request
- 401: errors related to JWT authentication and authorization
- 404: resource not found
- 405: method not allow
- 422: unprocessable action
- 500: internal server error

#### Endpoints

- <u>GET /actors</u>
  - Description:

    - Return a list of actors

  - Authorization:

    - It requires "view actors" permission

  - Sample call: 

    ```
    source setup.sh
    curl localhost:8080/actors -H "Authorization: bearer ${ASSISTANT_JWT}"
    ```

  - Output:

    ```
    {
      "actors": [
        {
          "age": 23,
          "gender": "M",
          "id": 27,
          "movies_id": [
            10
          ],
          "name": "Peter"
        },
        {
          "age": 24,
          "gender": "M",
          "id": 28,
          "movies_id": [],
          "name": "Martin"
        }
      ],
      "success": true,
      "total_actors": 2
    }
    
    ```

- <u>GET /movies:</u>

  - Description:

    - Return a list of movies

  - Authorization:

    - It requires "view movies" permission

  - Sample call: 

    ```
    source setup.sh
    curl localhost:8080/movies -H "Authorization: bearer ${ASSISTANT_JWT}"
    ```

  - Output:

    ```
    {
      "movies": [
        {
          "actors_id": [
            27
          ],
          "date_release": "20200330",
          "id": 10,
          "title": "Genesis"
        }
      ],
      "success": true,
      "total_movies": 1
    }
    ```

- <u>DELETE /actors/<integer: actor_id></u>

  - Description:

    - Delete an actor with the specified actor_id, return success in state or error otherwise

  - Authorization:

    - It requires "delete actors" permission

  - Sample call: 

    ```
    source setup.sh
    curl -X DELETE localhost:8080/actors/28 -H "Authorization: bearer ${DIRECTOR_JWT}"
    ```

  - Output:

    ```
    {
      "actor_id": 28,
      "success": true
    }
    ```

- <u>DELETE /movies/<integer: movie_id></u>

  - Description:

    - Delete a movie with the specified movie_id, return success in state or error otherwise

  - Authorization:

    - It requires "delete movies" permission

  - Sample call: 

    ```
    source setup.sh
    curl -X DELETE localhost:8080/movies/10 -H "Authorization: bearer ${PRODUCER_JWT}"
    ```

  - Output:

    ```
    {
      "movie_id": 10,
      "success": true
    }
    ```

- <u>POST /actors/</u>

  - Description:

    - Add an actor into the system, return success in state or error otherwise

  - Authorization:

    - It requires "create actors" permission

  - The values pass in the post body are:

    | name                 | type and value   |
    | -------------------- | ---------------- |
    | name                 | string           |
    | age                  | integer          |
    | gender               | enum: "M" or "F" |
    | movies_id (optional) | integer array    |

  - Sample call: 

    ```
    source setup.sh
    curl -X POST localhost:8080/actors -H "Authorization: bearer ${DIRECTOR_JWT}" -H "Content-type: application/json" -d '{"name":"Mangus", "age":38, "gender":"M"}'
    ```

  - Output:

    ```
    {
      "actor_id": 29,
      "success": true
    }
    ```

- <u>POST /movies/</u>

  - Description:

    - Add a movie into the system, return success in state or error otherwise
    - In passing the values into the system, actors_id must be passed

  - Authorization:

    - It requires "create movies" permission

  - The values pass in the post body are:

    | name         | type and value      |
    | ------------ | ------------------- |
    | title        | string              |
    | date_release | string ("YYYYMMDD") |
    | actors_id    | integer array       |

  - Sample call: 

    ```
    source setup.sh
    curl -X POST localhost:8080/movies -H "Authorization: bearer ${PRODUCER_JWT}" -H "Content-type: application/json" -d '{"title":"Genesis II", "date_release":"20200403", "actors_id":[29]}'
    ```

  - Output:

    ```
    {
      "movie_id": 11,
      "success": true
    }
    ```

- <u>PATCH /actors/<integer: actor_id></u>

  - Description:

    - Update an actor with the specified actor_id in the system, return success in state or error otherwise

  - Authorization:

    - It requires "modify actors" permission

  - The values pass in the post body are:

    | name                 | type and value   |
    | -------------------- | ---------------- |
    | name                 | string           |
    | age                  | integer          |
    | gender               | enum: "M" or "F" |
    | movies_id (optional) | integer array    |

  - Sample call: 

    ```
    source setup.sh
    curl -X PATCH localhost:8080/actors/29 -H "Authorization: bearer ${DIRECTOR_JWT}" -H "Content-type: application/json" -d '{"name":"Mangus", "age":30, "gender":"M"}'
    ```

  - Output:

    ```
    {
      "actor_id": 29,
      "success": true
    }
    ```

- <u>PATCH /movies/<integer: movie_id</u>

  - Description:

    - Update a movie with the specified movie_id in the system, return success in state or error otherwise
    - In passing the values into the system, actors_id must be passed

  - Authorization:

    - It requires "modify movies" permission

  - The values pass in the post body are:

    | name         | type and value      |
    | ------------ | ------------------- |
    | title        | string              |
    | date_release | string ("YYYYMMDD") |
    | actors_id    | integer array       |

  - Sample call: 

    ```
    source setup.sh
    curl -X PATCH localhost:8080/movies/11 -H "Authorization: bearer ${PRODUCER_JWT}" -H "Content-type: application/json" -d '{"title":"Genesis II", "date_release":"20200412", "actors_id":[29]}'
    ```

  - Output:

    ```
    {
      "movie_id": 11,
      "success": true
    }
    ```
