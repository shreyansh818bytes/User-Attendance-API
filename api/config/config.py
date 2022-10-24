import os
from datetime import timedelta

from decouple import config

BASE_DIR = os.path.dirname(os.path.realpath(__file__))


import os


class Config:
    SECRET_KEY = config("SECRET_KEY")
    JWT_SECRET_KEY = config("JWT_SECRET_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(minutes=30)

    # Database Environment Variables
    DB_USERNAME = config("DB_USERNAME")
    DB_PASSWORD = config("DB_PASSWORD")
    DB_HOSTNAME = config("DB_HOSTNAME")
    DB_NAME = config("DB_NAME")
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_NAME}"
    )


class DevConfig(Config):
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True
    DEBUG = True


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


config_dict = {"dev": DevConfig, "testing": TestConfig}
