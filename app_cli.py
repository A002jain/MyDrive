from db_file import db, User, add_to_db


def _get_admin():
    return User.query.filter_by(user_name='admin').first()


def _cli_input():
    email = input("Enter New Email Id: ")
    password = input("Enter Admin Password: ")
    return email, password


def admin_exist():
    admin = _get_admin()
    if admin is None:
        print("Admin did not exist")
        create_admin()
        admin = _get_admin()
    return admin


def reset_app():
    print("Deleting all data include admin data")
    if verify_admin():
        db.drop_all()


def create_admin():
    print("Creating Admin with UserName 'admin'")
    user_name = "admin"
    email, password = _cli_input()
    add_to_db(email, user_name, password)


def update_admin():
    print("Just press enter if don't want to change existing data")
    admin = _get_admin()
    print(str(admin))
    email, password = _cli_input()
    if email != "":
        admin.email = email
    if password != "":
        admin.password = password
    db.session.commit()


def verify_admin():
    admin = admin_exist()
    print("Verify Admin")
    email, password = _cli_input()
    if admin.email == email and admin.password == password:
        return True
    return False
