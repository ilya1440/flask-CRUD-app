# Udacity Capstone Final Project
Simple Flask-based application that features SQLAlchemy model definition, endpoints configuration, unit testing, RBAC functionality and deployment on Render.

## Setting up the Backend

### Install Dependencies

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

2. **Virtual Environment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organized. Instructions for setting up a virual environment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

3. **PIP Dependencies** - Once your virtual environment is setup and running, install the required dependencies by navigating to the `/backend` directory and running:

```bash
pip install -r requirements.txt
```

#### Key Pip Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use to handle the lightweight SQL database. You'll primarily work in `app.py`and can reference `models.py`.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross-origin requests from our frontend server.

### Run the Server

From within the `./backend` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask python run.py
```

The `--reload` flag will detect file changes and restart the server automatically.

## API Reference

### Getting Started
- Base URL: Render live URL `https://capstone-deployment.onrender.com/` The backend app can be run locally with the default URL `http://127.0.0.1:5000/`. 
- Authentication: The authentication system used for this project is Auth0. The Auth0 JWT includes claims for permissions based on the user's role within the Auth0 system. To test endpoints under particular role one should authorize with provided email and password or use provided JWT token. There are following three roles:
  - Casting Assistant
     - can `get:actors`
     - can `get:movies`
   - Casting Director
     - can perform all actions Casting Assistant can
     - can `create:actor`
     - can `delete:actor`
     - can `modify:actor`
     - can `modify:movie`
   - Executive Producer
     - can perform all actions Casting Director can
     - can `create:movie`
     - can `delete:movie`

### Error Handling
Errors are returned as JSON objects in the following format:
```
{
    "success": False, 
    "error": 400,
    "message": "bad request"
}
```
The API will return following error types when requests fail:
- 400: Bad Request
- 404: Resource Not Found
- 422: Not Processable 
- 403: Authorization Error

### Expected endpoints and behaviors

` curl --request GET --url  http://127.0.0.1:5000/movies --header 'authorization: Bearer {ACCESS_TOKEN}`

- Fetches a list of movies
- Request Arguments: None
- Returns: An object with a key, movies, that contains dictionaries of movies, and a success key.

```json
{
  "movies": [
    {
      "id":1,
      "release_date":"Wed, 01 Jan 2014 00:00:00 GMT",
      "title":"Big Short"
    }
  ],
  "success": true,
}
```

---
` curl --request GET --url  http://127.0.0.1:5000/actors --header 'authorization: Bearer {ACCESS_TOKEN}`

- Fetches a list of actors
- Request Arguments: None
- Returns: An object with a key, actors, that contains dictionaries of actors, and a success key.

```json
{
  "actors": [
    {
      "age":48,
      "gender":"Male",
      "id":1,
      "name":"Christian Bale"
    }
  ],
  "success": true,
}
```

---
`curl --request POST --url  http://127.0.0.1:5000/movies --header 'Content-Type: application/json' --header 'authorization: Bearer {ACCESS_TOKEN}' --data '{"title": "Avatar", "release_date": "2023-01-01"}'`

- Sends a post request in order to add a new movie
- Returns: ID of created movie and success value

```json
{
  "created": 2,
  "success": true
}
```

---
`curl --request POST --url  http://127.0.0.1:5000/actors --header 'Content-Type: application/json' --header 'authorization: Bearer {ACCESS_TOKEN}' --data '{"age": 42, "name": "Ryan Gosling", "gender": "Male"}'`

- Sends a post request in order to add a new movie
- Returns: ID of created movie and success value

```json
{
  "created": 2,
  "success": true
}
```

---
`curl --request DELETE --url  http://127.0.0.1:5000/movies/1 --header 'authorization: Bearer {ACCESS_TOKEN}'`

- Sends a delete request in order to delete a movie
- Request Arguments: `id` - integer
- Returns: ID of deleted movie and success value

```json
{
  "deleted": 1,
  "success": true
}
```

---
`curl --request DELETE --url  http://127.0.0.1:5000/actors/1 --header 'authorization: Bearer {ACCESS_TOKEN}'`

- Sends a delete request in order to delete an actor
- Request Arguments: `id` - integer
- Returns: ID of deleted actor and success value

```json
{
  "deleted": 1,
  "success": true
}
```

---
`curl --request PATCH --url  http://127.0.0.1:5000/actors/1 --header 'Content-Type: application/json' --header 'authorization: Bearer {ACCESS_TOKEN}' --data '{"age": 42, "name": "Ryan Gosling", "gender": "Male"}'`

- Sends a patch request in order to modify an existing actor
- Request Arguments: `id` - integer
- Returns: ID of modified actor and success value

```json
{
  "modified": 1,
  "success": true
}
```
---
`curl --request PATCH --url  http://127.0.0.1:5000/movies/1 --header 'Content-Type: application/json' --header 'authorization: Bearer {ACCESS_TOKEN}' --data '{"title": 'Avatar', "release_date": "2023-01-01"}'`

- Sends a patch request in order to modify an existing movie
- Request Arguments: `id` - integer
- Returns: ID of modified movie and success value

```json
{
  "modified": 1,
  "success": true
}
```

## Testing

To deploy the tests, run

```bash
python test_app.py
```

