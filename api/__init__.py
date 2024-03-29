from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api

from api.attendance.views import attendance_namespace
from api.auth.views import auth_namespace
from api.config.config import config_dict
from api.models.absentee import Absentee
from api.models.user import User
from api.users.views import users_namespace
from api.utils.db import db


def create_app(config=config_dict["dev"]):
    app = Flask(__name__)

    app.config.from_object(config)

    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Add a JWT with ** Bearer &lt;JWT&gt; to authorize",
        }
    }

    api = Api(
        app,
        title="User Attendance API",
        description="A REST API for monitoring staff attendance.",
        authorizations=authorizations,
        security="Bearer Auth",
    )

    api.add_namespace(auth_namespace, path="/auth")
    api.add_namespace(users_namespace)
    api.add_namespace(attendance_namespace)

    db.init_app(app)

    JWTManager(app)

    Migrate(app, db)

    @app.shell_context_processor
    def make_shell_context():
        return {
            "db": db,
            "User": User,
            "Absentee": Absentee,
        }

    return app
