from flask import session, redirect, url_for, request, Blueprint, render_template, jsonify
from db_file import get_from_db, ban_user, add_to_folder_db, get_folder_db_data, delete_folder_from_db, update_folder_db
from db_file import delete_user_from_db, verified_user
from custum_decorators import admin_role

admin_bp = Blueprint("admin", __name__)


@admin_bp.route("/settings")
@admin_role
def admin_panel():
    return render_template("setting.html", users=get_from_db(), folders=get_folder_db_data())


@admin_bp.route("/remove_user", methods=['POST'])
@admin_role
def remove_user():
    user_id = request.form['user_id']
    delete_user_from_db(user_id)
    return redirect(url_for('admin.admin_panel'))


@admin_bp.route("/ban", methods=['POST'])
@admin_role
def banned_user():
    user_id = request.form['ban_user_id']
    ban_user(user_id)
    return redirect(url_for('admin.admin_panel'))


@admin_bp.route("/add_folder", methods=['POST'])
@admin_role
def add_folders():
    folder_path = request.form['shared_folder_path']
    time_period = request.form['time_period']
    add_to_folder_db(folder_path, time_period)
    return redirect(url_for('admin.admin_panel'))


@admin_bp.route("/remove_folder", methods=['POST'])
@admin_role
def remove():
    folder_id = request.form['folder_id']
    delete_folder_from_db(folder_id)
    return redirect(url_for('admin.admin_panel'))


@admin_bp.route("/update_folder", methods=['POST'])
@admin_role
def update():
    folder_id = request.form['folder_id']
    enable = request.form.get('enable_folder')
    time_period = request.form['time_period']
    update_folder_db(folder_id, enable, time_period)
    return redirect(url_for('admin.admin_panel'))


@admin_bp.route("/activate", methods=['POST'])
@admin_role
def activate_user():
    activate_user_id = request.form['activate_user']
    verified_user(activate_user_id)
    return redirect(url_for('admin.admin_panel'))


@admin_bp.route('/test/session', methods=['GET'])
def test_session_data():
    meta_data = {
        'username': session.get('username'),
        'email': session.get('email'),
        'current_path': session.get('currentPath'),
        'verified': session.get('verified'),
        'current_video_path': session.get('current_video_path'),
        'video_list': session.get('video_list')
    }
    return jsonify(meta_data)


