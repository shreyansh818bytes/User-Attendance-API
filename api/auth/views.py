from flask_restx import Resource, Namespace, fields, reqparse
from api.models.user import User, UserRole
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    get_jwt_identity,
)
from werkzeug.exceptions import Conflict, BadRequest

auth_namespace = Namespace("auth", description="Authentication Namespace")


register_request_parser = reqparse.RequestParser()
register_request_parser.add_argument("name", type=str, help="Full Name of the user")
register_request_parser.add_argument("email", type=str, help="Email of the user")
register_request_parser.add_argument(
    "password", type=str, help="Password for user's account"
)
register_request_parser.add_argument("role", type=UserRole, help="Role of the new user")


user_model = auth_namespace.model(
    "User",
    {
        "id": fields.Integer(),
        "name": fields.String(required=True, description="Full Name"),
        "email": fields.String(required=True, description="An email"),
        "is_active": fields.Boolean(description="This shows that User is active"),
        "role": fields.String(description="Role of the user"),
    },
)

login_request_parser = reqparse.RequestParser()
login_request_parser.add_argument("email", type=str, help="Email linked User account")
login_request_parser.add_argument(
    "password", type=str, help="Password set for user login"
)


@auth_namespace.route("/register")
class Register(Resource):
    @auth_namespace.expect(register_request_parser, validate=True)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
        Create a new user account
        """

        data = register_request_parser.parse_args()
        try:

            new_user = User(
                name=data.get("name"),
                email=data.get("email"),
                password_hash=generate_password_hash(data.get("password")),
                role=data.get("role", UserRole.MEMBER),
            )

            new_user.save()

            return new_user, HTTPStatus.CREATED

        except Exception as e:
            raise Conflict(f"User with email {data.get('email')} exists")


@auth_namespace.route("/login")
class Login(Resource):
    @auth_namespace.expect(login_request_parser)
    def post(self):
        """
        Generate a JWT

        """

        data = login_request_parser.parse_args()

        email = data.get("email")
        password = data.get("password")

        user = User.query.filter_by(email=email).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.email)
            refresh_token = create_refresh_token(identity=user.email)

            response = {"acccess_token": access_token, "refresh_token": refresh_token}

            return response, HTTPStatus.OK

        raise BadRequest("Invalid email or password")


@auth_namespace.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    def post(self):
        email = get_jwt_identity()

        access_token = create_access_token(identity=email)

        return {"access_token": access_token}, HTTPStatus.OK
