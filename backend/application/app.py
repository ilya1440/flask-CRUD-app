from flask import request, jsonify, abort
from flask_cors import CORS
from werkzeug.exceptions import HTTPException
from dateutil.parser import parse

from .database.models import db_drop_and_create_all, setup_db, Movie, Actor
from .auth.auth import AuthError, requires_auth

from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db_drop_and_create_all()

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "GET, POST, PATCH, DELETE, OPTIONS")
        return response

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies():
        try:
            movies = Movie.query.all()
            movies = [movie.format() for movie in movies]
            return jsonify(
                {
                    "success": True,
                    "movies": movies
                }
            )
        except:
            abort(400)

    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors():
        try:
            actors = Actor.query.all()
            actors = [actor.format() for actor in actors]
            return jsonify(
                {
                    "success": True,
                    "actors": actors
                }
            )
        except:
            abort(400)

    @app.route('/movies', methods=['POST'])
    @requires_auth('create:movie')
    def create_movie():
        try:
            body = request.get_json()
            title = body.get('title', None)
            release_date = body.get('release_date', None)
            try:
                parse(release_date)
            except ValueError:
                abort(422)
            movie = Movie(title=title, release_date=release_date)
            movie.insert()
            return jsonify(
                {
                    "success": True,
                    "created": movie.id
                }
            )
        except HTTPException as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(422)

    @app.route('/actors', methods=['POST'])
    @requires_auth('get:actor')
    def create_actor():
        try:
            body = request.get_json()
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)
            actor = Actor(name=name, age=age, gender=gender)
            if not isinstance(age, int):
                abort(422)
            actor.insert()
            return jsonify(
                {
                    "success": True,
                    "created": actor.id
                }
            )
        except HTTPException as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(422)

    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth('delete:movie')
    def delete_movie(id):
        try:
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            if not movie:
                abort(404)
            movie.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": id
                }
            )
        except HTTPException as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(422)

    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actor')
    def delete_actor(id):
        try:
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if not actor:
                abort(404)
            actor.delete()
            return jsonify(
                {
                    "success": True,
                    "deleted": id
                }
            )
        except HTTPException as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(422)

    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('modify:movie')
    def modify_movie(id):
        try:
            body = request.get_json()
            title = body.get('title', None)
            release_date = body.get('release_date', None)
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            try:
                parse(release_date)
            except ValueError:
                abort(422)
            if not movie:
                abort(404)
            movie.title = title
            movie.release_date = release_date
            movie.update()
            return jsonify(
                {
                    "success": True,
                    "modified": movie.id
                }
            )
        except HTTPException as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(422)

    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('modify:actor')
    def modify_actor(id):
        try:
            body = request.get_json()
            name = body.get('name', None)
            age = body.get('age', None)
            gender = body.get('gender', None)
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            if not isinstance(age, int):
                abort(422)
            if not actor:
                abort(404)
            actor.name = name
            actor.age = age
            actor.gender = gender
            actor.update()
            return jsonify(
                {
                    "success": True,
                    "modified": actor.id
                }
            )
        except HTTPException as e:
            if isinstance(e, HTTPException):
                abort(e.code)
            else:
                abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 404,
                "message": "resource not found"
            }
        ), 404

    @app.errorhandler(400)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 400,
                "message": "bad request"
            }
        ), 400

    @app.errorhandler(422)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": 422,
                "message": "unprocessable entity"
            }
        ), 422

    @app.errorhandler(AuthError)
    def not_found(error):
        return jsonify(
            {
                "success": False,
                "error": error.error,
                "message": "authorization error"
            }
        ), error.status_code

    return app
