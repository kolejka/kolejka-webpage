#!/usr/bin/env python3
# vim:ts=4:sts=4:sw=4:expandtab

SECRET_PATH = 'github_secret'
PUSH_PATH = 'github_push'
BIN_PATH = 'bin/github_push'

import datetime
from multiprocessing import Process
import os
from pathlib import Path
import pwd
import subprocess
import sys
import tempfile

def result(code, status, body, exit=True):
    sys.stdout.write('Status: {} {}\r\n'.format(code, status))
    sys.stdout.write('Content-Length: {}\r\n'.format(len(body)))
    sys.stdout.write('\r\n')
    sys.stdout.write('{}'.format(body))
    if exit:
        sys.exit(0)

home = Path.home()
if not home.is_dir():
    home = Path(pwd.getpwuid(os.getuid()).pw_dir)
secret_path = home / SECRET_PATH

secret = ''
if not secret_path.is_file():
    result(500, 'Internal Server Error', 'FAIL')
with secret_path.open() as secret_file:
    secret = secret_file.read().strip()

if os.environ.get('QUERY_STRING','') != 'secret={}'.format(secret):
    result(403, 'Forbidden', 'FAIL')

if os.environ.get('REQUEST_METHOD','').upper() != 'POST':
    result(403, 'Forbidden', 'FAIL')

body = sys.stdin.read()


push_path = home / PUSH_PATH
push_path.mkdir(parents=True, exist_ok=True)
push_fd, push_path = tempfile.mkstemp(dir=str(push_path), prefix='{}_'.format(datetime.datetime.now().strftime('%Y%m%d%H%M%S')))
os.write(push_fd, bytes(sys.stdin.read(), 'utf-8'))

result(200, 'OK', 'OK', exit=False)
#sys.stdout.close()

handle_path = home / BIN_PATH

if handle_path.is_file():
    handle_path = str(handle_path)
    def child():
        os.execv(handle_path, [handle_path, push_path])
    Process(target=child).start()
