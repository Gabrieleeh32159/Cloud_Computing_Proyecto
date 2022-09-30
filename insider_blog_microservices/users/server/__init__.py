from argparse import _AttributeHolder
from datetime import datetime, timedelta
import json
from pickle import TRUE
import uuid
import psycopg2
from flask import (
    Flask,
    abort,
    jsonify,
    make_response,
    request
)
import jwt
from functools import wraps
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
from models import setup_db, User, Post, GroupUser, Group

default_image = 'default.jpg'

items_per_page = 5


def pagination(request, selection, decreasing=False):
    page = request.args.get('page', None, type=int)
    if page is None and not decreasing:
        start = 0
        end = 5
    elif page == 0:
        start = 0
        end = len(selection)
    elif decreasing:
        start = len(selection) - items_per_page
        end = len(selection)
        items = [item.format() for item in selection]
        current = items[start:end]
        return current[::-1]
    else:
        start = (page - 1)*items_per_page
        end = (start + items_per_page)
    items = [item.format() for item in selection]
    current = items[start:end]
    return current


def create_app(test_config=None):
    app = Flask(__name__)
    setup_db(app)
    CORS(app, origin=['http://127.0.0.1:3000/'], max_age=1000)

    @app.after_request
    def after_request(response):
        #response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PATCH,POST,DELETE,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    #*USERS

    def token_required(f):
        @wraps(f)
        def decorator(*args, **kwargs):
            token = None
            if 'x-access-tokens' in request.headers:
                token = request.headers['x-access-tokens']

            if not token:
                return jsonify({'message': 'a valid token is missing'})

            try:
                data = jwt.decode(
                    token, app.config['SECRET_KEY'], algorithms=['HS256'])
                current_user = User.query.filter_by(
                    public_id=data['public_id']).first()
                if current_user is None:
                    return jsonify({'message': 'token is invalid'})
            except Exception as e:
                print(e)
                return jsonify({'message': 'token is invalid'})

            return f(current_user, *args, **kwargs)
        return decorator

    @app.route('/users', methods=['GET'])
    def get_users():
        users = [user.format() for user in User.query.order_by('id').all()]

        if len(users) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'users': users,
            'amount_users': len(users)
        })

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        body = request.get_json()

        username = body.get('username', None)
        description = body.get('description', '')
        email = body.get('email', None)
        password = body.get('password', None)
        image = body.get('image', default_image)

        if username is None or email is None or password is None:
            abort(422)

        hashed_password = generate_password_hash(
            body['password'], method='sha256')

        user = User(public_id=str(uuid.uuid4()), username=username, description=description,
                    email=email, password=hashed_password, image_file=image)

        user.insert()
        return jsonify({
            'success': True
        })

    @app.route('/users', methods=['POST'])
    def create_user():
        body = request.get_json()

        if body is None:
            abort(422)

        username = body.get('username', None)
        description = body.get('description', '')
        email = body.get('email', None)
        password = body.get('password', None)
        image = body.get('image', default_image)

        if username is None or email is None or password is None:
            abort(422)

        if username is "" or email is "" or password is "":
            abort(422)

        hashed_password = generate_password_hash(
            body['password'], method='sha256')

        user = User(public_id=str(uuid.uuid4()), username=username, description=description,
                    email=email, password=hashed_password, image_file=image)

        new_user_id = user.insert()
        group_user = GroupUser(group_id=0, user_id=new_user_id)
        group_user.insert()

        selection = User.query.order_by('id').all()
        current_users = pagination(request, selection, True)

        return jsonify({
            'success': True,
            'created': new_user_id,
            'total_users': len(selection),
            'user': user.format()
        })

    @app.route('/user', methods=['GET'])
    def verify():
        auth = request.headers['Authorization']
        if auth is None:
            return make_response('No auth', 403, {'WWW.Authentication': 'Token Required'})

        token = auth.replace('Bearer ', '')

        print(token)

        data = jwt.decode(
            token, app.config['SECRET_KEY'], algorithms=['HS256'])
        current_user = User.query.filter_by(
            public_id=data['public_id']).first()
        if current_user is None:
            return jsonify({'message': 'token is invalid'})

        return current_user.format()

    @app.route('/login', methods=['GET', 'POST'])
    def login_user():
        auth = request.authorization
        if not auth or not auth.username or not auth.password:
            return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

        user = User.query.filter_by(username=auth.username).first()

        if check_password_hash(user.password, auth.password):
            token = jwt.encode({'public_id': user.public_id, 'exp': datetime.utcnow(
            ) + timedelta(minutes=30)}, app.config['SECRET_KEY'])
            return jsonify({
                'token': token,
                'user': user.format()
            })

        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    @app.route('/users/<user_id>', methods=['PATCH'])
    def update_user(user_id):
        error_404 = False
        try:
            user = User.query.filter(User.id == user_id).one_or_none()

            if user is None:
                error_404 = True
                abort(404)

            body = request.get_json()
            if 'username' in body:
                if body.get('username') != "":
                    user.username = body.get('username')
            if 'email' in body:
                if body.get('email') != "":
                    user.email = body.get('email')
            if 'password' in body:
                if body.get('password') != "":
                    user.password = body.get('password')
            if 'description' in body:
                if body.get('description') != "":
                    user.description = body.get('description')

            if body.get('username') == "" and body.get('email') == "" and body.get('password') == "" and body.get('description') == "":
                abort(422)

            user.update()

            return jsonify({
                'success': True,
                'id': user_id
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/users/<user_id>', methods=['DELETE'])
    def delete_user(user_id):
        error_404 = False
        try:
            user = User.query.filter(User.id == user_id).one_or_none()

            if user is None:
                error_404 = True
                abort(404)

            user.delete()

            selection = User.query.order_by('id').all()
            users = pagination(request, selection)

            return jsonify({
                "success": True,
                "deleted": user_id,
                "users": users,
                "total_users": len(selection)
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    # ! ERROR HANDLERS

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'code': 404,
            'message': 'resource not found'
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            'success': False,
            'code': 500,
            'message': 'Internal Server error'
        }), 500

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            'success': False,
            'code': 422,
            'message': 'Unprocessable'
        }), 422

    @app.route('/')
    def index():
        return "Insider's blog API"

    return app
