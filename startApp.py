from flask import Flask, session, redirect, url_for, request, send_file
from flask import render_template
import os
from werkzeug.utils import secure_filename
from streaming import bp
from users import bp as user_bp
from utils import change_dir, provide_dir_path, drives, userList, generic_file_listing, get_os, UPLOAD_FOLDER


# style="background-image: url('{{ url_for('static',filename='images/image.jpg') }}');"
# https://stackoverflow.com/questions/40460846/using-flask-inside-class
# https://flask.palletsprojects.com/en/1.1.x/patterns/fileuploads/

# Flask setting
app = Flask(__name__)
app.secret_key = b'_5#y2L";[.3z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.register_blueprint(bp)
app.register_blueprint(user_bp)


@app.route('/')
def index():
    if 'username' in session:
        return render_template('home.html', loginas=session['username'])
    return redirect(url_for('user.login'))


@app.route('/drive', methods=['GET', 'POST'])
def drive():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    list_files = generic_file_listing(path=provide_dir_path())
    return render_template('drive.html', name='FileExplorer', list=list_files, drive_name=drives,
                           os_name=get_os())


@app.route('/back', methods=['GET', 'POST'])
def back():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    change_dir("..")
    if request.referrer == request.host_url + "drive":
        return redirect(url_for('drive'))
    else:
        return redirect(url_for("stream.media_video"))


@app.route('/download/<index_x>', methods=['GET', 'POST'])
def download(index_x):
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    print(index_x)
    if index_x.find(".") == -1:
        print("*" * 100)
        print(index_x)
        change_dir(index_x)
        return redirect(url_for('drive'))
    path = provide_dir_path() + "/" + index_x
    print(path)
    return send_file(path, as_attachment=True)


@app.route('/switchDrive/<index_x>')
@app.route('/switchDrive', methods=['GET'])
def switch_drive(index_x=None):
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    if index_x is None:
        change_dir("switch#Drive")
    else:
        change_dir("switch#Drive#"+str(index_x))
    if request.referrer == request.host_url + "drive":
        return redirect(url_for('drive'))
    else:
        return redirect(url_for("stream.media_video"))


# ###################UPLOAD####################################################

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
        print(app.config['UPLOAD_FOLDER'])
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("file saved")
    return redirect(url_for('upload2'))
# https://www.w3schools.com/howto/howto_css_navbar_icon.asp


@app.route('/user/listing', methods=['GET'])
def listing():
    print(userList)
    return str(session)


if __name__ == "__main__":
    app.run(host="192.168.43.53", debug=True)
    # app.run(debug=True)