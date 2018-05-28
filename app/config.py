from flask_env import MetaFlaskEnv

class Configuration(metaclass=MetaFlaskEnv):
    UPLOAD_FOLDER = "/tmp/covered/uploads"
