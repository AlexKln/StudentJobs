from flask_restful import Resource, reqparse
from flask_jwt_extended import (create_access_token, jwt_required)
from models import User

parser = reqparse.RequestParser()
parser.add_argument('username', help = 'This field cannot be blank', required = True)
parser.add_argument('password', help = 'This field cannot be blank', required = True)


class UserRegistration(Resource):
    def post(self):
        data = parser.parse_args()

        if data['username'] == "" or data['password'] == "":
            return {'message': 'Fields cant be blank'}, 502

        if User.find_by_username(data['username']):
            return {'message': 'User {} already exists'.format(data['username'])}, 502

        new_user = User(
            username=data['username'],
            password=User.generate_hash(data['password'])
        )

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=data['username'])
            return {
                'message': 'User {} was created'.format(data['username']),
                'access_token': access_token
            }, 200
        except:
            return {'message': 'Something went wrong'}, 502


class UserLogin(Resource):
    def post(self):
        data = parser.parse_args()
        current_user = User.find_by_username(data['username'])

        if data['username'] == "" or data['password'] == "":
            return {'message': 'Fields cant be blank'}, 502

        if not current_user:
            return {'message': 'User {} doesn\'t exist'.format(data['username'])}, 502

        if User.verify_hash(data['password'], current_user.password):
            access_token = create_access_token(identity=data['username'])
            return {
                'message': 'Logged in as {}'.format(current_user.username),
                'access_token': access_token
            }, 200
        else:
            return {'message': 'Wrong credentials'}, 502


# class UserLogoutAccess(Resource):
#     def post(self):
#         return {'message': 'User logout'}


# class UserLogoutRefresh(Resource):
#     def post(self):
#         return {'message': 'User logout'}


# class TokenRefresh(Resource):
#     def post(self):
#         return {'message': 'Token refresh'}


# class AllUsers(Resource):
#     def get(self):
#         return User.return_all()
#
#     def delete(self):
#         return User.delete_all()


class ValidateToken(Resource):
    @jwt_required
    def get(self):
        return {
            'answer': 'OK'
        }
