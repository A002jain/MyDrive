import click
from flask.cli import with_appcontext
from db_file import add_to_db
from db_instance import db


@click.command(name='add_admin')
@with_appcontext
def add_admin():
    email = "adhi@god.com"
    password = "god"
    user_name = "admin"
    add_to_db(email=email,
              password=password,
              user_name=user_name,
              verified=True)


@click.command(name='init_db')
@with_appcontext
def init_db():
    db.create_all()


@click.command(name='reset_db')
@with_appcontext
def reset_db():
    db.drop_all()
