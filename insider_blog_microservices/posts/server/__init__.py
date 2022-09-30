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

    #* POSTS
    @app.route('/posts', methods=['POST'])
    def create_post():
        body = request.get_json()
        user_id = body.get('user_id', None)
        group_id = body.get('group_id', None)
        title = body.get('title', None)
        content = body.get('content', None)

        user = User.query.filter(User.id == user_id).one_or_none()
        group = Group.query.filter(Group.id == group_id).one_or_none()

        if title is None or content is None:
            abort(422)

        if user is None or group is None:
            abort(404)

        if title is "" or content is "":
            abort(422)

        if user is "" or group is "":
            abort(404)

        post = Post(title=title, content=content,
                    user_id=user_id, group_id=group_id)

        post_id = post.insert()

        selection = Post.query.filter(
            Post.group_id == group_id and Post.user_id == user_id).order_by('id').all()
        current_posts = pagination(
            request=request, selection=selection, decreasing=True)
        return jsonify({
            'success': True,
            'id': post_id,
            'posts': current_posts,
            'created': post_id
        })

    @app.route('/posts', methods=['GET'])
    def get_posts():
        user_id = request.args.get('user_id', None, type=int)
        user = User.query.filter(User.id == user_id).one_or_none()

        group_id = request.args.get('group_id', None, type=int)
        group = Group.query.filter(Group.id == group_id).one_or_none()

        if (user_id is not None and user is None) or (group_id is not None and group is None):
            abort(404)

        #* Obtener posts en un grupo
        if user_id is None and group_id is not None:
            selection = Post.query.filter(
                Post.group_id == group_id).order_by('id').all()
        #* Obtener posts de una persona
        elif group_id is None and user_id is not None:
            selection = Post.query.filter(
                Post.user_id == user_id).order_by('id').all()
        #* Obtener posts de un usuario en un grupo
        elif group_id is not None and user_id is not None:
            selection = Post.query.filter(
                Post.user_id == user_id and Post.group_id == group_id).order_by('id').all()
        #* Obtener todos los posts
        elif group_id is None and user_id is None:
            selection = Post.query.order_by('id').all()

        posts = pagination(
            request=request, selection=selection, decreasing=True)
        posts2 = pagination(request, selection)

        if len(posts) == 0 or len(posts2) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'posts': posts,
            'amount_posts': len(selection)
        })

    @app.route('/posts/<int:post_id>', methods=['PATCH'])
    def update_post(post_id):
        error_404 = False
        try:
            post = Post.query.filter(Post.id == post_id).one_or_none()

            if post is None:
                error_404 = True
                abort(404)

            body = request.get_json()

            if 'title' in body:
                post.title = body.get('title')
            if 'content' in body:
                post.content = body.get('content')
            post.update()

            return jsonify({
                'success': True,
                'id': post_id
            })
        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/posts/<int:post_id>', methods=['DELETE'])
    def delete_post(post_id):
        error_404 = False
        try:
            post = Post.query.filter(Post.id == post_id).one_or_none()

            if post is None:
                error_404 = True
                abort(404)

            post.delete()

            selection = Post.query.order_by('id').all()
            current_posts = pagination(
                request=request, selection=selection, decreasing=True)

            return jsonify({
                'success': True,
                'id': post_id,
                'posts': current_posts,
                'amount_posts': len(selection)
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
