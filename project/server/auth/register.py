import jwt

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email

from flask import make_response, jsonify
from flask.views import MethodView

from project.server import db, app
from project.server.models import User


class RegisterForm(FlaskForm):
    email = StringField('Ім\'я', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    submit = SubmitField('Реєстрація')


class RegisterAPI(MethodView):
    """
    User Registration Resource
    """

    def post(self):
        # get the post data

        form = RegisterForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            # check if user already exists
            print()
            user = User.query.filter_by(email=email).first()
            if not user:
                try:
                    user = User(
                        email=email,
                        password=password
                    )
                    # insert the user
                    db.session.add(user)
                    db.session.commit()
                    # generate the auth token
                    auth_token = user.encode_auth_token(user.id)
                    print("AUTH TOKEN:::", auth_token)
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully registered.',
                        'auth_token': jwt.decode(auth_token, app.config.get('SECRET_KEY'), algorithms=["HS256"])
                    }
                    return make_response(jsonify(response_object)), 201
                except Exception as e:
                    response_object = {
                        'status': 'fail',
                        'message': 'Some error occurred. Please try again.'
                    }
                    print(e)
                    return make_response(jsonify(response_object)), 401
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'User already exists. Please Log in.',
                }
                return make_response(jsonify(response_object)), 202
        response_object = {
            'status': 'fail',
            'message': 'Invalid form submission.'
        }
        return make_response(jsonify(response_object)), 400
