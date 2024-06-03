# project/server/auth/__init__.py
# define the API resources
from flask import Blueprint, request

from project.server.auth.login import LoginAPI
from project.server.auth.logout import LogoutAPI
from project.server.auth.register import RegisterAPI

from .login import LoginAPI, LoginForm
from .logout import LogoutAPI
from .register import RegisterAPI, RegisterForm
from .userAPI import UserAPI, check_status


auth_blueprint = Blueprint('auth', __name__)




registration_view = RegisterAPI.as_view('register_api')
login_view = LoginAPI.as_view('login_api')
user_view = UserAPI.as_view('user_api')
logout_view = LogoutAPI.as_view('logout_api')

# add Rules for API Endpoints
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST']
)
auth_blueprint.add_url_rule(
    '/auth/status',
    view_func=user_view,
    methods=['GET']
)
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST']
)