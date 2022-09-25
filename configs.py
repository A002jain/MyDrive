from pathlib import Path
""" Flask application config """

# # Flask settings
# SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
#
# UPLOAD_FOLDER = str(Path.home()) + "/Downloads"
#
# # Flask-SQLAlchemy settings
# SQLALCHEMY_DATABASE_URI = 'sqlite:///drive_db.db'  # File-based SQL database
# SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning

upload_folder = str(Path.home()) + "/Downloads"


# Class-based application configuration
class ConfigClass:
    """ Flask application config """

    # Flask settings
    SECRET_KEY = 'This is an INSECURE secret!! DO NOT use this in production!!'
    # SESSION_COOKIE_SECURE = True

    UPLOAD_FOLDER = str(Path.home()) + "/Downloads"

    # Flask-SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = 'sqlite:///drive_db.db'  # File-based SQL database
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoids SQLAlchemy warning
