import hashlib, json, sys, os
from datetime import datetime
from typing import Tuple

from qa_std.qa_app_info import ConfigurationFile, Configuration, BuildType, BIH


def _write_bih_(bih: BIH) -> None:
    o = {
        'srel': bih.S_REL_N,
        'brel': bih.B_REL_N,
        'arel': bih.A_REL_N,
        'bid': bih.BUILD_ID,
        'rel_date': bih.REL_DATE
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
        S_REL_N=r_json['srel'], B_REL_N=r_json['brel'], A_REL_N=r_json['arel'],
        BUILD_ID=r_json['bid'], REL_DATE=r_json['rel_date']
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
    assert bl.pop(0) == '4'
    assert len(bl) == 3

    s, b, al = map(lambda x: int(x), bl)

    match build_type:
        case BuildType.ALPHA:
            _bih.A_REL_N += 1
            al += 1

        case BuildType.BETA:
            _bih.B_REL_N += 1
            b += 1
            al += 1

        case BuildType.STABLE:
            _bih.S_REL_N += 1
            s += 1
            b += 1
            al += 1

        case _:
            raise NotImplementedError

    _bid = build_type.name[0]
    _bid += f"_{hashlib.md5(f'{_rel_date}'.encode()).hexdigest()[-8::]}{_rel_date.strftime('%H%M')}"

    _bih.BUILD_ID = _bid
    _bih.REL_DATE = _rel_date.strftime('%b %d, %Y %H:%M:%S')

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
    print(f'... Wrote to BIH: {bih.BUILD_ID} @ {bih.REL_DATE}')

    _write_config_(conf)
    print(f'... Wrote to CONF')

    print(f'... Running MyPy tests.')
    os.system('mypy --pretty --disallow-untyped-defs --disallow-incomplete-defs --check-untyped-defs --no-implicit-optional --warn-redundant-casts --warn-return-any --disallow-untyped-globals --allow-redefinition --show-error-context --show-column-numbers --show-error-codes --pretty --disallow-any-generics .')

    print(f'... Running PyTest tests.')
    os.system('pytest -vv .')

    sys.exit(0)
