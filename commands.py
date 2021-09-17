import click
from flask.cli import with_appcontext
from db_file import add_to_db


@click.command(name='add_admin')
@with_appcontext
def create_tables():
    email = "adhi@god.com"
    password = "god"
    user_name = "admin"
    add_to_db(email=email,
              password=password,
              user_name=user_name,
              verified=True)
