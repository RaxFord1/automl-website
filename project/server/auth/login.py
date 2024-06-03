import jwt

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from flask import request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, app
from project.server.models import User


class LoginForm(FlaskForm):
    email = StringField('Ім\'я', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Увійти')


class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):
        # get the post data
        print("Login in")
        post_data = request.get_json()
        print("Request Form")
        print(request.form)

        email = request.form['email']
        password = request.form['password']
        try:
            # fetch the user data
            user = User.query.filter_by(
                email=email
            ).first()
            print("ASDSADASD")
            if user and bcrypt.check_password_hash(
                    user.password, password
            ):
                auth_token = user.encode_auth_token(user.id)
                if auth_token:
                    auth_tocket_jwt = jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms=["HS256"])

                    print("LOGIN:::", auth_token, auth_tocket_jwt, type(auth_token))
                    responseObject = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                        'auth_token': auth_token.decode("UTF-8"),
                        'email': email
                    }
                    print("Response Obj")
                    print(responseObject)
                    return make_response(jsonify(responseObject)), 200
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'User does not exist.'
                }
                return make_response(jsonify(responseObject)), 404
        except Exception as e:
            print("EXCEPTION::::")
            print(e)
            responseObject = {
                'status': 'fail',
                'message': 'Try again'
            }
            return make_response(jsonify(responseObject)), 500
