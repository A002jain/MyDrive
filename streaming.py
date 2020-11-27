from __future__ import print_function
import logging
import os
import re
import mimetypes
import subprocess as sb
from flask import (
    Response, Blueprint, redirect, render_template, request, session
)

bp = Blueprint('stream', __name__)
global PATH
LOG = logging.getLogger(__name__)
VIDEO_PATH = '/video'
MB = 1 << 20
BUFF_SIZE = 10 * MB
global listFiles


@bp.route('/media', methods=['GET', 'POST'])
def media_video():
    global listFiles
    global PATH
    PATH = sb.Popen("pwd", shell=True, stdout=sb.PIPE, stdin=sb.PIPE, stderr=sb.PIPE).stdout.read().decode()[:-1] + "/"
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    files_x = sb.Popen("ls", shell=True, stdout=sb.PIPE, stdin=sb.PIPE, stderr=sb.PIPE)
    listFiles = files_x.stdout.read().decode().split("\n")[:-1]
    return render_template('streamMedia.html', list=listFiles, dirLength=len(listFiles))


@bp.route('/back1', methods=['GET', 'POST'])
def back():
    if 'username' not in session:
        return "login first <a href='/login'>login</a>"
    os.chdir("..")
    return redirect('/media')


@bp.route('/stream/<int:media>')
def home(media):
    global listFiles
    print(listFiles[media])
    LOG.info('Rendering home page')
    if listFiles[media].find(".") == -1:
        print("*" * 100)
        os.chdir(listFiles[media])
        return redirect('/media')
    response = render_template('streaming.html', video=VIDEO_PATH + "/" + str(media))
    return response


def partial_response(path, start, end=None):
    LOG.info('Requested: %s, %s', start, end)
    file_size = os.path.getsize(path)

    # Determine (end, length)
    if end is None:
        end = start + BUFF_SIZE - 1
    end = min(end, file_size - 1)
    end = min(end, start + BUFF_SIZE - 1)
    length = end - start + 1

    # Read file
    with open(path, 'rb') as fd:
        fd.seek(start)
        bytes_x = fd.read(length)
    assert len(bytes_x) == length

    response = Response(
        bytes_x,
        206,
        mimetype=mimetypes.guess_type(path)[0],
        direct_passthrough=True,
    )
    response.headers.add(
        'Content-Range', 'bytes {0}-{1}/{2}'.format(
            start, end, file_size,
        ),
    )
    response.headers.add(
        'Accept-Ranges', 'bytes'
    )
    LOG.info('Response: %s', response)
    LOG.info('Response: %s', response.headers)
    return response


def get_range(request_x):
    range_x = request_x.headers.get('Range')
    LOG.info('Requested: %s', range_x)
    m = re.match('bytes=(?P<start>\d+)-(?P<end>\d+)?', range_x)
    if m:
        start = m.group('start')
        end = m.group('end')
        start = int(start)
        if end is not None:
            end = int(end)
        return start, end
    else:
        return 0, None


@bp.route(VIDEO_PATH + "/<int:file>")
def video(file):
    global PATH
    global listFiles
    path = PATH + listFiles[file]
    print(path)
    start, end = get_range(request)
    return partial_response(path, start, end)
