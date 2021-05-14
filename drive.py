from flask import Blueprint, session, redirect, url_for, request, send_file
from flask import render_template
import os
from werkzeug.utils import secure_filename
from utils import change_dir, provide_dir_path, drives, generic_file_listing, get_os, UPLOAD_FOLDER
from custum_decorators import login_required, check_ban_user
drive_bp = Blueprint('drive', __name__)


@drive_bp.before_request
@check_ban_user
def check_user_data():
    pass


@drive_bp.route('/drive', methods=['GET', 'POST'])
@login_required
def drive():
    list_files = generic_file_listing(path=provide_dir_path())
    return render_template('drive.html', name='FileExplorer', list=list_files, drive_name=drives,
                           os_name=get_os())


@drive_bp.route('/back', methods=['GET', 'POST'])
@login_required
def back():
    change_dir("..")
    if request.referrer == request.host_url + "drive":
        return redirect(url_for('drive.drive'))
    else:
        return redirect(url_for("stream.media_video"))


@drive_bp.route('/download/<tag>', methods=['GET', 'POST'])
@login_required
def download(tag=None):
    # print(tag)
    if tag.find(".") == -1:
        # print("*" * 100)
        # print(tag)
        change_dir(tag)
        return redirect(url_for('drive.drive'))
    path = provide_dir_path() + "/" + tag
    # print(path)
    return send_file(path, as_attachment=True)


@drive_bp.route('/switchDrive/<tag>')
@drive_bp.route('/switchDrive', methods=['GET'])
@login_required
def switch_drive(tag=None):
    if tag is None:
        change_dir("switch#Drive")
    else:
        change_dir("switch#Drive#"+str(tag))
    if request.referrer == request.host_url + "drive":
        return redirect(url_for('drive.drive'))
    else:
        return redirect(url_for("stream.media_video"))


# ###################UPLOAD####################################################

@drive_bp.route('/upload1')
@login_required
def upload1():
    return render_template('upload.html')


@drive_bp.route('/upload2')
@login_required
def upload2():
    return render_template('upload2.html')


@drive_bp.route('/uploadFile', methods=['POST'])
@login_required
def uploadFile():
    # if request.method == 'POST':
    #     # print("POST")
    if 'files[]' not in request.files:
        # flash('No file part')
        # print(request.url)
        return redirect(request.url)
    files = request.files.getlist('files[]')
    for file in files:
        filename = secure_filename(file.filename)
        # print(UPLOAD_FOLDER)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        # print("file saved")
    return redirect(url_for('drive.upload2'))
# https://www.w3schools.com/howto/howto_css_navbar_icon.asp
