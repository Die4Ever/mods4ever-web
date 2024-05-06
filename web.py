# flask --app web.py run --debug --port 10451
# or just python3 web.py
from flask import Flask, redirect, render_template, request, g
import requests
import dateutil.parser
from apis.projects import get_projects

from dxlog.base import *
from dxlog.handler import handle_telem
from apis import dxrando

app = Flask(__name__,
            static_url_path='/public', 
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


@app.route('/dxrando/writebingo', methods=["POST"])
def writebingo():
    if request.args.get('adminpassword', '') != get_config().get('adminpassword'):
        return {'error': 'bad password'}, 401
    return dxrando.writebingo(request.get_data())

@app.route('/api/dxrando/leaderboard')
def api_dxrando_leaderboard():
    try:
        SortBy = request.args.get('SortBy', 'score')
        Grouped = request.args.get('Grouped', True)
        GameMode = request.args.get('GameMode', -1)
        return dxrando.leaderboard(SortBy=SortBy, Grouped=Grouped, GameMode=GameMode)
    except Exception as e:
        logex(e)
        raise

@app.route('/dxrando/leaderboard')
def dxrando_leaderboard():
    return render_template('dxrando/leaderboard.jinja2')

@app.route('/project/<path:path>/downloads')
def downloads(path):
    g.project = get_projects().get(path)
    if not g.project:
        return redirect('/', code=302)
    repo = g.project.get('repo')
    if not repo:
        return redirect('/', code=302)
    data = requests.get('https://api.github.com/repos/' + repo + '/releases').content
    data = json.loads(data)
    out = []
    prevTime = datetime.datetime.now(datetime.timezone.utc)
    for release in data:
        r = {}
        published = release.get('published_at')
        published = dateutil.parser.isoparse(published)
        r = dict(name=release.get('name'), published=published.isoformat())

        total = 0
        for asset in release.get('assets'):
            count = int(asset.get('download_count'))
            r[asset.get('name')] = count
            total += count
        r['total'] = total

        delta:datetime.timedelta = prevTime - published
        r['per_day'] = round(total / (delta.total_seconds()/86400), 1)
        if release.get('name') != 'Development Build':
            prevTime = published
        out.append(r)
    out = json.dumps(out, indent='&nbsp;&nbsp;&nbsp;&nbsp;')
    return out.replace('\n', '<br/>\n')

@app.route('/project/<path:path>')
def project(path):
    g.project = get_projects().get(path)
    if not g.project:
        return redirect('/', code=302)
    return render_template('project.jinja2')


@app.route('/')
@app.route('/<path:path>')
@app.route('/<path:path>/')
def catch_all(path=None):
    if path:
        p = path.lower()
        if 'discord' == p:
            return redirect('https://discord.gg/ZBEfrEPS8e')
        if 'lemmy' == p:
            return redirect('https://lemmy.mods4ever.com/?listingType=Local&sort=New')
        if 'kbin' == p:
            return redirect('https://kbin.social/m/meta@lemmy.mods4ever.com/t/193090/Mods4Ever-FAQ-and-Links')
        if 'mbin' == p:
            return redirect('https://kbin.run/m/meta@lemmy.mods4ever.com/t/403048/Mods4Ever-FAQ-and-Links') # the domain name says kbin but they run mbin now
        if 'mastodon' == p:
            return redirect('https://mastodon.gamedev.place/@Die4ever')
        if 'youtube' == p:
            return redirect('https://www.youtube.com/playlist?list=PLZIQTa_kwZhBksj7UzcahPiRaHk87fWch')
    
    g.projects = get_projects()
    return render_template('base.jinja2')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=10451)
