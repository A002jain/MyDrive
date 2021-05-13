from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    verified = db.Column(db.Boolean(), nullable=False, server_default='0')
    banned = db.Column('is_banned', db.Boolean(), nullable=False, server_default='0')

    # User authentication information. The collation='NOCASE' is required
    # to search case insensitively when USER_IFIND_MODE is 'nocase_collation'.

    email = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False, server_default='')

    user_name = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='')


class Folders(db.Model):
    __tablename__ = 'folders'
    id = db.Column(db.Integer, primary_key=True)
    share_enabled = db.Column('share_enabled', db.Boolean(), nullable=False, server_default='1')

    folder_path = db.Column(db.String(100, collation='NOCASE'), nullable=False, unique=True)

    time_period = db.Column(db.String(100, collation='NOCASE'), nullable=False, server_default='NONE')


def add_to_db(email, user_name, password):
    user_in_db = User(email=email, password=password, user_name=user_name)
    db.session.add(user_in_db)
    db.session.commit()


def get_from_db(filtering=None):
    if filtering is None:
        return User.query.all()
        # db_db = db.session.execute("select * from users")
    else:
        db_db = db.session.execute(f"select {filtering} from users")
    return db_db.fetchall()


def get_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    return user


def get_user_by_id(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user


def get_folder_by_id(folder_id):
    folder = Folders.query.filter_by(id=folder_id).first()
    return folder


def set_user_active(email, status):
    pass
    condition = User.email == email
    # set_user_active_dml_query = User.__table__.update().values({'is_active': status}).where(s)
    set_user_active_dml_query = generate_update_query(updated_values={'is_active': status}, where_condition=condition)
    db.session.execute(set_user_active_dml_query)
    db.session.commit()
    # active_user.active = status
    # db.session.commit()


def ban_user(user_id):
    # u = User.__table__.update().values({'is_banned': status}).where(User.id == user_id)
    condition = User.id == user_id
    user = get_user_by_id(user_id)
    user.banned = not user.banned
    # ban_user_dml_query = generate_update_query(updated_values={'is_banned': not status}, where_condition=condition)
    # db.session.execute(ban_user_dml_query)
    db.session.commit()


def generate_update_query(updated_values, where_condition):
    return User.__table__.update().values(updated_values).where(where_condition)


def get_folder_db_data():
    return Folders.query.order_by(Folders.id).all()


def add_to_folder_db(folder_path, time_period):
    if time_period is "":
        time_period = "NONE"
    folder_in_db = Folders(folder_path=folder_path, time_period=time_period)
    db.session.add(folder_in_db)
    db.session.commit()


def delete_folder_from_db(folder_id):
    folder = get_folder_by_id(folder_id)
    db.session.delete(folder)
    db.session.commit()


def delete_user_from_db(user_id):
    user = get_user_by_id(user_id)
    db.session.delete(user)
    db.session.commit()


def update_folder_db(folder_id, enable, time_period):
    updated_values = {
        'share_enabled': True if enable == "on" else False,
        'time_period': "NONE" if time_period is "" else time_period
    }
    folder_update_dml = Folders.__table__.update().values(updated_values).where(Folders.id == folder_id)
    db.session.execute(folder_update_dml)
    db.session.commit()
