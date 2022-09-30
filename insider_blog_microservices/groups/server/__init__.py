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

    #* GROUPS
    @app.route('/groups', methods=['POST'])
    #@token_required
    def create_group():
        error_422 = False
        try:
            body = request.get_json()

            groupname = body.get('groupname', None)

            if groupname is None:
                error_422 = True
                abort(422)

            if groupname is "":
                error_422 = True
                abort(422)

            group = Group(group_name=groupname)

            group_id = group.insert()
            print(group_id)

            selection = Group.query.order_by('id').all()
            current_groups = pagination(request, selection)

            return jsonify({
                'success': True,
                'created': group_id,
                'groups': current_groups,
                'total_groups': len(selection)
            })
        except Exception as e:
            print(e)
            if error_422:
                abort(422)
            else:
                abort(500)

    @app.route('/groups', methods=['GET'])
    def get_groups():
        error_404 = False
        try:
            groups = [group.format() for group in Group.query.order_by("id").all()]

            if len(groups) == 0:
                error_404 = True
                abort(404)

            return jsonify({
                'success': True,
                'grupos': groups,
                'total_groups': len(groups)
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)

    @app.route('/groups/<int:group_id>', methods=['DELETE'])
    def delete_group(group_id):
        error_404 = False
        try:
            group = Group.query.filter(Group.id == group_id).one_or_none()
            if group is None:
                error_404 = True
                abort(404)

            group.delete()

            selection = Group.query.order_by('id').all()
            groups = pagination(request, selection)

            return jsonify({
                "success": True,
                "deleted": group_id,
                "groups": groups,
                "total_groups": len(selection)
            })

        except Exception as e:
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/groups/<group_id>', methods=['PATCH'])
    def update_group(group_id):
        error_404 = False
        try:
            group = Group.query.filter(Group.id == group_id).one_or_none()

            if group is None:
                error_404 = True
                abort(404)

            body = request.get_json()

            if 'groupname' in body:
                group.group_name = body.get('groupname')

            group.update()

            return jsonify({
                'success': True,
                'id': group_id
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    #* UNIR USUARIOS A GRUPOS
    @app.route('/user/<int:user_id>/group/<int:group_id>', methods=['POST'])
    def join_user_group(user_id, group_id):
        error_404 = False
        try:
            user = User.query.filter(User.id == user_id).one_or_none()
            group = Group.query.filter(Group.id == group_id).one_or_none()

            if user is None or group is None:
                error_404 = True
                abort(404)

            groupuser = GroupUser(user_id=user_id, group_id=group_id)
            groupuser.insert()

            return jsonify({
                'success': True
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    #* BORRAR USUARIOS DE UN GRUPO
    @app.route('/group/<int:group_id>/user/<int:user_id>', methods=['DELETE'])
    def delete_user_from_group(group_id, user_id):
        error_404 = False
        try:
            user = User.query.filter(User.id == user_id).one_or_none()
            group = Group.query.filter(Group.id == group_id).one_or_none()

            if user is None or group is None:
                error_404 = True
                abort(404)

            groupuser = GroupUser.query.filter(
                GroupUser.user_id == user_id and GroupUser.group_id == group_id).one_or_none()
            groupuser.delete()

            return jsonify({
                'success': True
            })

        except Exception as e:
            print(e)
            if error_404:
                abort(404)
            else:
                abort(500)

    @app.route('/groupusers', methods=['GET'])
    def get_groupusers():
        selection = GroupUser.query.order_by('user_id').all()
        groupusers = pagination(request, selection)

        if len(groupusers) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'groupusers': groupusers,
            'total_groupusers': len(selection)
        })

    @app.route('/group/<group_id>/user/<user_id>', methods=['PATCH'])
    def update_group_user(group_id, user_id):
        error_404 = False
        try:
            gropuser = GroupUser.query.filter(
                GroupUser.user_id == user_id).one_or_none()

            if gropuser is None:
                error_404 = True
                abort(404)

            body = request.get_json()
            if 'group_id' in body:
                group_new_id = body.get('group_id')
                gropuser.group_id = body.get('group_id')

            gropuser.update()

            return jsonify({
                'success': True,
                'id': group_new_id
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
