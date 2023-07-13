# flask --app api.py run --debug --port 10451
# or just python3 api.py
from flask import Flask, request

from dxlog.base import *
from dxlog.handler import handle_telem

app = Flask(__name__)

@app.route('/dxrando/log.py', methods=["GET", "POST"])
def telem():
    ip = request.remote_addr
    if ip is None:
        warn('no REMOTE_ADDR?')
        return
    data = request.get_data()
    params = request.args
    return handle_telem(data, ip, params)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    return 'You want path: %s' % path

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=10451)
