import hashlib, json, sys, os
from datetime import datetime
from typing import Tuple

from qa_std.qa_app_info import ConfigurationFile, Configuration, BuildType, BIH


def _write_bih_(bih: BIH) -> None:
    o = {
        "r_stbl":
        {
            "n": bih.S_REL_N,
            "dc": bih.S_DC
        },
        "r_beta":
        {
            "n": bih.B_REL_N,
            "dc": bih.B_DC
        },
        "r_alph":
        {
            "n": bih.A_REL_N,
            "dc": bih.A_DC
        }
    }

    with open(r'.conf\_BIH.json', 'w') as _bih:
        _bih.write(json.dumps(o, indent=4))
        _bih.close()

    del o


def _load_bih_() -> BIH:
    with open(r'.conf\_BIH.json', 'r') as _bih:
        r_str = _bih.read()
        _bih.close()

    r_json = json.loads(r_str)

    return BIH(
        S_REL_N=r_json['r_stbl']['n'],
        S_DC=r_json['r_stbl']['dc'],
        B_REL_N=r_json['r_beta']['n'],
        B_DC=r_json['r_beta']['dc'],
        A_REL_N=r_json['r_alph']['n'],
        A_DC=r_json['r_alph']['dc']
    )


def _load_config_() -> Configuration:
    ConfigurationFile.load_file()
    assert ConfigurationFile.config._ver == 1, 'Invalid Configuration construct.'

    return ConfigurationFile.config


def _write_config_(config: Configuration) -> None:
    assert config._ver == 1, 'Invalid Configuration construct.'

    o = json.dumps({
        'build':
            {
                "AUTH": ["Geetansh Gautam", "geetansh.ca"],
                "AVS": config.AVS,
                "BT": config.BT.value,
                "BI": config.BI
            },
        'settings':
            {
                "locale": [int(config.locale[0]), config.locale[1]],
                "LOG_VERB": config.VLE
            }
    }, indent=4)

    with open(r'.conf\configuration.json', 'w') as _conf:
        _conf.write(o)
        _conf.close()


def _gen_bih_(
    build_type: BuildType
) -> Tuple[BIH, Configuration]:
    _bih = _load_bih_()
    _rel_date = datetime.now()

    _conf = _load_config_()

    bl = _conf.AVS.split('.')
    assert bl.pop(0) == '4'                     # Make sure that this configuration is for the 4th version of the app
    assert len(bl) == 3                         # Version info

    s, b, al = map(lambda x: int(x), bl)

    # Date code
    _dc = int(_rel_date.strftime('%y%m%d%H%M%S'))

    # Build ID
    _bid = build_type.name[0]
    _bid += f"_{_dc}_{hashlib.md5(f'{_dc}'.encode()).hexdigest()[-8::]}"

    match build_type:
        case BuildType.ALPHA:
            al += 1 if '--DNI' not in sys.argv else 0
            _bih.A_DC = _bid

        case BuildType.BETA:
            b += 1 if '--DNI' not in sys.argv else 0
            _bih.B_DC = _bid

        case BuildType.STABLE:
            s += 1 if '--DNI' not in sys.argv else 0
            _bih.S_DC = _bid

        case _:
            raise NotImplementedError

    _bih.A_REL_N = al
    _bih.B_REL_N = b
    _bih.S_REL_N = s

    # _bih.BUILD_ID = _bid

    avs = f"4.{s}.{b}.{al}"

    _conf.AVS = avs
    _conf.BT = build_type
    _conf.BI = _bid

    return _bih, _conf


if __name__ == "__main__":
    print('QA4 | Build')
    print('  Sets up the configuration files for a new release.')
    print('     --stable................. for a stable release')
    print('     --beta................... for a beta release')
    print('     --alpha.................. for an alpha release')
    print('')
    print('  Other options')
    print('     --no-tests............... do not run tests')
    print('     --DNI.................... do not increment build n-value')

    assert \
        '--stable' in sys.argv or \
        '--beta' in sys.argv or \
        '--alpha' in sys.argv, \
        'Specify whether the release is a stable, beta, or alpha release.'

    bt = BuildType.ALPHA

    for a in sys.argv:
        if a in ('--stable', '--beta', '--alpha'):
            bt = {
                '--stable': BuildType.STABLE,
                '--beta': BuildType.BETA,
                '--alpha': BuildType.ALPHA
            }[a]

            break

    bih, conf = _gen_bih_(bt)

    _write_bih_(bih)
    print(f'... Wrote to BIH: {conf.BI} @ {conf.AVS}')

    _write_config_(conf)
    print(f'... Wrote to CONF')

    print(f'... Running MyPy tests.')
    os.system(
        'mypy --pretty --disallow-untyped-defs --disallow-incomplete-defs --check-untyped-defs '
        '--no-implicit-optional --warn-redundant-casts --warn-return-any --disallow-untyped-globals '
        '--allow-redefinition --show-error-context --show-column-numbers --show-error-codes --pretty '
        '--disallow-any-generics .'
    )

    if '--no-tests' not in sys.argv:
        print(f'... Running PyTest tests.')
        os.system('pytest -vv .')

    sys.exit(0)
