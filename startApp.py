from flask import Flask, session, redirect, url_for, request, send_file, flash
from flask import render_template
import subprocess as sb
import os
from werkzeug.utils import secure_filename
from streaming import bp
from users import bp as user_bp
from utils import change_dir, provide_dir_path, drives, userList

HOME_DIR = "/home/abhinav/"
UPLOAD_FOLDER = "/home/abhinav/Downloads"

# https://stackoverflow.com/questions/40460846/using-flask-inside-class
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

# Flask setting
app = Flask(__name__)
app.secret_key = b'_5#y2L";[.3z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(bp)
app.register_blueprint(user_bp)


# def change_dir(directory):
# 	current_drive = session['currentDrive']
# 	if directory == "switchDrive":
# 		drives.reverse()
# 		print(drives)
# 		session['currentDrive'] = drives[0][1]
# 	elif directory != "..":
# 		session['currentDrive'] = current_drive + "/" + directory
# 	else:
# 		print("back")
# 		current_drive = current_drive[:-1] if current_drive[-1] == "/" else current_drive
# 		tmp = current_drive.split("/")[1:-1]
# 		current_drive = ""
# 		for i in tmp:
# 			current_drive = current_drive + "/" + i
# 			session['currentDrive'] = current_drive
#
#
# def provide_dir_path():
# 	return session['currentDrive']


@app.route('/')
def index():
    if 'username' in session:
        return render_template('home.html', loginas=session['username'])
    return redirect(url_for('user.login'))


@app.route('/drive', methods=['GET', 'POST'])
def drive():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    cmd = "ls " + provide_dir_path()
    print(cmd)
    files_x = sb.Popen(cmd, shell=True, stdout=sb.PIPE, stdin=sb.PIPE, stderr=sb.PIPE)
    list_files = files_x.stdout.read().decode().split("\n")[:-1]
    return render_template('drive.html', name='FileExplorer', list=list_files, currentDrive=drives[0][0],switchDrive=drives[1][0])


@app.route('/back', methods=['GET', 'POST'])
def back():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    change_dir("..")
    return redirect(url_for('drive'))


@app.route('/download/<index>', methods=['GET', 'POST'])
def download(index):
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    print(index)
    if index.find(".") == -1:
        print("*" * 100)
        print(index)
        change_dir(index)
        return redirect(url_for('drive'))
    path = provide_dir_path() + "/" + index
    print(path)
    return send_file(path, as_attachment=True)


@app.route('/switchDrive', methods=['GET'])
def switch_drive():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    change_dir("switchDrive")
    return redirect(url_for('drive'))


####################UPLOAD####################################################

@app.route('/upload1')
def upload1():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    return render_template('upload.html')


@app.route('/upload2')
def upload2():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    print("again")
    return render_template('upload2.html')


@app.route('/uploadFile', methods=['POST'])
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
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("file saved")
    return redirect(url_for('upload2'))
# https://www.w3schools.com/howto/howto_css_navbar_icon.asp


@app.route('/ser/listing', methods=['GET'])
def listing():
    print(userList)
    return str(session)
