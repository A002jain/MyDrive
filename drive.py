from flask import Blueprint, session, redirect, url_for, request, send_file
from flask import render_template
import os
from werkzeug.utils import secure_filename

from utils import change_dir, provide_dir_path, drives, generic_file_listing, get_os, UPLOAD_FOLDER

drive_bp = Blueprint('drive', __name__)


@drive_bp.route('/')
def index():
    if 'username' in session:
        return render_template('home.html', loginas=session['username'])
    return redirect(url_for('user.login'))


@drive_bp.route('/drive', methods=['GET', 'POST'])
def drive():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    list_files = generic_file_listing(path=provide_dir_path())
    return render_template('drive.html', name='FileExplorer', list=list_files, drive_name=drives,
                           os_name=get_os())


@drive_bp.route('/back', methods=['GET', 'POST'])
def back():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    change_dir("..")
    if request.referrer == request.host_url + "drive":
        return redirect(url_for('drive.drive'))
    else:
        return redirect(url_for("stream.media_video"))


@drive_bp.route('/download/<index_x>', methods=['GET', 'POST'])
def download(index_x):
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    print(index_x)
    if index_x.find(".") == -1:
        print("*" * 100)
        print(index_x)
        change_dir(index_x)
        return redirect(url_for('drive.drive'))
    path = provide_dir_path() + "/" + index_x
    print(path)
    return send_file(path, as_attachment=True)


@drive_bp.route('/switchDrive/<index_x>')
@drive_bp.route('/switchDrive', methods=['GET'])
def switch_drive(index_x=None):
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    if index_x is None:
        change_dir("switch#Drive")
    else:
        change_dir("switch#Drive#"+str(index_x))
    if request.referrer == request.host_url + "drive":
        return redirect(url_for('drive.drive'))
    else:
        return redirect(url_for("stream.media_video"))


# ###################UPLOAD####################################################

@drive_bp.route('/upload1')
def upload1():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    return render_template('upload.html')


@drive_bp.route('/upload2')
def upload2():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    print("again")
    return render_template('upload2.html')


@drive_bp.route('/uploadFile', methods=['POST'])
def uploadFile():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    if request.method == 'POST':
        print("POST")
    if 'files[]' not in request.files:
        # flash('No file part')
        print(request.url)
        return redirect(request.url)
    files = request.files.getlist('files[]')
    for file in files:
        filename = secure_filename(file.filename)
        print(UPLOAD_FOLDER)
        file.save(os.path.join(UPLOAD_FOLDER, filename))
        print("file saved")
    return redirect(url_for('drive.upload2'))
# https://www.w3schools.com/howto/howto_css_navbar_icon.asp
