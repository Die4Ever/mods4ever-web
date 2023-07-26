
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
            'links': {
                'OpenRCT2': 'https://openrct2.org/',
            },
        },
        'Unreal Tournament (1999) Crowd Control / Randomizer': {
            'repo': 'TheAstropath/UT99CrowdControl',
            'community': 'ut99_crowdcontrol',
            'links': {
                'OldUnreal Unreal Tournament 99 patch': 'https://github.com/OldUnreal/UnrealTournamentPatches/releases',
            },
        },
        'Build Engine Randomizer': {
            'repo': 'Die4Ever/build-engine-randomizer',
            'community': 'build_randomizer',
            'links': {
                'Wiki': 'https://github.com/Die4Ever/build-engine-randomizer/wiki',
            },
        },
        'StarCraft 2 Balance Patch Randomizer': {
            'repo': 'Die4Ever/starcraft-2-randomizer',
            'community': 'sc2_randomizer',
            'links': {
                'TL.net Discussion Thread': 'https://tl.net/forum/starcraft-2/575425-balance-patch-randomizer-mod#1',
            },
        },
        'Unreal Randomizer': {
            'repo': 'Die4Ever/unreal-randomizer',
            'community': 'unreal_randomizer',
            'links': {
                'Unreal patch 227i': 'https://www.oldunreal.com/downloads/unreal/oldunreal-patches/',
            },
        },
        'Duke Nukem Forever 2001 Restoration Project Randomizer': {
            'repo': 'Die4Ever/dnf2001-randomizer',
            'community': 'dnf_randomizer',
            'links': {
                'Duke Nukem Forever 2001: Restoration Project': 'https://www.moddb.com/mods/dnf2001-restoration-project',
            },
        },
        'Stream Detective': {
            'repo': 'TheAstropath/StreamDetective',
            'community': 'stream_detective',
        },
        'ScummVM Groovie (The 7th Guest, The 11th Hour...)': {
            'description': 'I mostly worked on The 11th Hour, Clandestiny, Tender Loving Care, and Uncle Henry\'s Playhouse.<br/>But also some improvements to The 7th Guest, like the new option for Easier AI.',
            'repo': 'scummvm/scummvm',
            'community': 'stauf_mansion',
            'links': {
                "Stauf's Mansion Discord": 'https://discord.gg/Hss5cJg',
                'ScummVM Website': 'https://www.scummvm.org/',
                'Downloads': 'https://www.scummvm.org/downloads/',
                'Demos': 'https://www.scummvm.org/demos/',
                'Wiki': 'https://wiki.scummvm.org/',
            },
        },
    }

    return d
