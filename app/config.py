from flask_env import MetaFlaskEnv


class Configuration(metaclass=MetaFlaskEnv):
    UPLOAD_FOLDER = "/tmp/covered/uploads"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
