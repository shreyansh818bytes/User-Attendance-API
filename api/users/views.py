from http import HTTPStatus

from flask_jwt_extended import jwt_required
from flask_restx import Namespace, Resource, fields

from api.models.user import User

users_namespace = Namespace("users", description="Users Namespace")

user_model = users_namespace.model(
    "User",
    {
        "id": fields.Integer(),
        "name": fields.String(required=True, description="Full Name"),
        "email": fields.String(required=True, description="An email"),
        "is_active": fields.Boolean(description="This shows that User is active"),
        "role": fields.String(description="Role of the user"),
    },
)


@users_namespace.route("/all")
class GetAllUsers(Resource):
    @users_namespace.marshal_with(user_model)
    @users_namespace.doc(description="Retrieve all users")
    @jwt_required()
    def get(self):
        """
        Fetch all users
        """

        users = User.query.all()

        return users, HTTPStatus.OK


@users_namespace.route("/user/<int:user_id>")
class GetDeleteUserById(Resource):
    @users_namespace.marshal_with(user_model)
    @users_namespace.doc(
        description="Retrieve a user by id", params={"user_id": "User ID"}
    )
    @jwt_required()
    def get(self, user_id):
        """
        Get user by ID
        """

        user = User.get_by_id(user_id)

        return user, HTTPStatus.OK

    @users_namespace.doc(
        description="Delete a user by id", params={"user_id": "User ID"}
    )
    @jwt_required()
    def delete(self, user_id):
        """
        Delete user by ID
        """

        User.get_by_id(user_id).delete()

        return {"message": "User deleted successfuly!"}, HTTPStatus.OK
