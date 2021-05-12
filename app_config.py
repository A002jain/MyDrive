from flask import Flask
from streaming import stream_bp
from users import user_bp
from drive import drive_bp


def create_app():
    """ Flask application factory """

    # Create Flask app load app.config
    app = Flask(__name__)
    # app.config.from_object(__name__ + '.ConfigClass')
    app.config.from_pyfile("configs.py")
    # adding user Blueprint
    app.register_blueprint(stream_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(drive_bp)
    # Initialize Flask-SQLAlchemy
    return app
