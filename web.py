# flask --app web.py run --debug --port 10451
# or just python3 web.py
from flask import Flask, render_template, request, g

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
    return dxrando.leaderboard()

@app.route('/dxrando/leaderboard')
def dxrando_leaderboard():
    return render_template('dxrando/leaderboard.html')

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def catch_all(path):
    g.projects = get_projects()
    return render_template('base.html')

if __name__ == "__main__":
    from waitress import serve
    serve(app, host="0.0.0.0", port=10451)

def get_projects():
    d = {
        'Deus Ex Randomizer': {
            'repo': 'Die4Ever/deus-ex-randomizer',
            'community': 'deus_ex_randomizer',
            'downloads': {
                'Windows': 'DXRandoInstaller.zip',
                'Linux': 'DXRandoInstaller-Linux.zip',
            },
            'links': {
                'Leaderboard': '/dxrando/leaderboard',
                'DXRando Activity Bot': 'https://botsin.space/@DXRandoActivity',
            },
        },
        'RollerCoaster Tycoon Randomizer': {
            'repo': 'Die4Ever/rollercoaster-tycoon-randomizer',
            'community': 'rct_randomizer',
            'downloads': {
                #'': '',
            }
        },
        'Unreal Tournament (1999) Crowd Control / Randomizer': {
            'repo': 'TheAstropath/UT99CrowdControl',
            'community': 'ut99_crowdcontrol',
            'downloads': {
                #'': '',
            }
        },
        'Build Engine Randomizer': {
            'repo': 'Die4Ever/build-engine-randomizer',
            'community': 'build_randomizer',
            'downloads': {
                #'': '',
            }
        },
        'StarCraft 2 Randomizer': {
            'repo': 'Die4Ever/starcraft-2-randomizer',
            'community': 'sc2_randomizer',
            'downloads': {
                #'': '',
            }
        },
        'Unreal Randomizer': {
            'repo': 'Die4Ever/unreal-randomizer',
            'community': 'unreal_randomizer',
            'downloads': {
                #'': '',
            }
        },
        'Duke Nukem Forever 2001 Restoration Project Randomizer': {
            'repo': 'Die4Ever/dnf2001-randomizer',
            'community': 'dnf_randomizer',
            'downloads': {
                #'': '',
            }
        },
        'Stream Detective': {
            'repo': 'TheAstropath/StreamDetective',
            'community': 'stream_detective',
            'downloads': {
                #'': '',
            }
        },
    }

    for (k,v) in d.items():
        if 'downloads' not in v:
            v['downloads'] = {}
        if 'links' not in v:
            v['links'] = {}

    return d