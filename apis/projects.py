
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

