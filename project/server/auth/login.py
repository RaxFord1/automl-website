import jwt

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from flask import request, make_response, jsonify
from flask.views import MethodView

from project.server import bcrypt, app
from project.server.models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class LoginAPI(MethodView):
    """
    User Login Resource
    """

    def post(self):

        form = LoginForm()
        if form.validate_on_submit():
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
                        response_object = {
                            'status': 'success',
                            'message': 'Successfully logged in.',
                            'auth_token': auth_token.decode("UTF-8"),
                            'email': email
                        }
                        print("Response Obj")
                        print(response_object)
                        return make_response(jsonify(response_object)), 200
                else:
                    response_object = {
                        'status': 'fail',
                        'message': 'User does not exist.'
                    }
                    return make_response(jsonify(response_object)), 400
            except Exception as e:
                print("EXCEPTION::::")
                print(e)
                response_object = {
                    'status': 'fail',
                    'message': 'Try again'
                }
                return make_response(jsonify(response_object)), 500
        response_object = {
            'status': 'fail',
            'message': 'Invalid form'
        }
        return make_response(jsonify(response_object)), 400
