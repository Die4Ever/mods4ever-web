# flask --app web.py run --debug --port 10451
# or just python3 web.py
from flask import Flask, redirect, render_template, request, g
from apis.projects import get_projects

from dxlog.base import *
from dxlog.handler import handle_telem
from apis import dxrando

app = Flask(__name__,
            static_url_path='', 
            static_folder='public',# on the real server we use nginx
            template_folder='templates')

@app.route('/dxrando/log.py', methods=["GET", "POST"])
def telem():
    ip = request.remote_addr
    if ip is None:
        warn('no REMOTE_ADDR?')
        return
    data = request.get_data()
    params = request.args
    return handle_telem(data, ip, params)

@app.route('/api/dxrando/leaderboard')
def api_dxrando_leaderboard():
    SortBy = request.args.get('SortBy', 'score')
    return dxrando.leaderboard(SortBy=SortBy)

@app.route('/dxrando/leaderboard')
def dxrando_leaderboard():
    return render_template('dxrando/leaderboard.jinja2')

@app.route('/project/<path:path>')
def project(path):
    g.project = get_projects().get(path)
    if not g.project:
        return redirect('/', code=302)
    return render_template('project.jinja2')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    g.projects = get_projects()
    return render_template('base.jinja2')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=10451)
