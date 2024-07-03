"""
FILE:           qa_update/qa_update.py
AUTHOR:         Geetansh Gautam
PROJECT:        Quizzing Application, version 4

DOC

    Defines functions for the auto-update system.

DEFINES


DEPENDENCIES

    qa_std
        AppInfo

"""

import urllib3, sys, json, traceback as tb, time
from typing import Optional, Callable, Any, Tuple, Dict, cast, Union

from qa_std import AppInfo


URL = 'https://raw.githubusercontent.com/GeetanshGautam0/QAS4/%s/.conf/_BIH.json'
HTTP = urllib3.PoolManager(
    timeout=urllib3.Timeout(connect=2.0, read=3.0),
    retries=False,
    headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache', 'Expires': 'Thu, 01 Jan 1970 00:00:00 GMT'}
)
CHANNELS = {
    AppInfo.BuildType.ALPHA: URL % 'alpha',
    AppInfo.BuildType.BETA: URL % 'beta',
    AppInfo.BuildType.STABLE: URL % 'stable',
}


def tr(f: Callable[[Any], Any], *args: Any, **kwargs: Any) -> Tuple[bool, Any]:
    try:
        return True, f(*args, **kwargs)

    except Exception as E:
        return False, E


def check_for_updates() -> Tuple[bool, str, str]:
    global URL, HTTP

    """
    New release system:
    
        Branch: release
        
        1. GET the BIH file from the branch.
        2. CHECK the 'n' value for each stream.
        3. LOG each 'n' value higher than that of the current installation. 
        4. DOWNLOAD data if the 'n' value for a stream with better or equal stability than the selected stream is greater
                    than the current installation. 
        5. RUN QA_INSTALLER. 
    
    """
    url = URL % 'release'  # Configure the URL to load the BIH from the release branch.

    sys.stdout.write(f'Trying to access {url} via the HTTP protocol ...\n')
    success, res = tr(  # type: ignore
        HTTP.request,   # type: ignore
        'GET',
        url,
        headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache', 'Expires': 'Thu, 01 Jan 1970 00:00:00 GMT'}
    )

    if not success:
        sys.stderr.write(f'[HTTP GET ERROR] Failed to access URL: {str(res)}')
        return False, AppInfo.ConfigurationFile.config.BI, AppInfo.ConfigurationFile.config.AVS

    http_response = cast(urllib3.BaseHTTPResponse, res)
    if http_response.status != 200:
        sys.stderr.write(f'[HTTP GET ERROR] Failed to access URL: Status {http_response.status}')
        return False, AppInfo.ConfigurationFile.config.BI, AppInfo.ConfigurationFile.config.AVS

    success, js = tr(json.loads, tr(http_response.data.decode)[1])  # type: ignore

    if not success:
        sys.stderr.write(f'[HTTP GET ERROR] Failed to access URL: JSON Decode Error')
        return False, AppInfo.ConfigurationFile.config.BI, AppInfo.ConfigurationFile.config.AVS

    j = cast(Dict[str, Any], js)

    try:

        srv = {
            AppInfo.BuildType.STABLE.value: j['r_stbl']['n'],
            AppInfo.BuildType.BETA.value: j['r_beta']['n'],
            AppInfo.BuildType.ALPHA.value: j['r_alph']['n']
        }

    except Exception as _:

        sys.stderr.write("[WARN] Could not retrieve version information from GitHub server.\r\n")
        time.sleep(0.1)
        sys.stderr.writelines(['\t |\t%s\r\n' % s for s in tb.format_exc().split('\n')])

        return False, AppInfo.ConfigurationFile.config.BI, AppInfo.ConfigurationFile.config.AVS

    # else:

    # Load the configuration info from the BIH file data downloaded.

    bl = AppInfo.ConfigurationFile.config.AVS.split('.')
    assert bl.pop(0) == '4'  # Make sure that this configuration is for the 4th version of the app
    assert len(bl) == 3      # Version info

    vc = list(map(lambda x: int(x), bl))[::-1]  # [A, B, S]
    pop = AppInfo.ConfigurationFile.config.BT.value  # Items to pop
    tc:  Union[Tuple[int], Tuple] = ()  # type: ignore

    for i in range(pop, 3):
        sys.stdout.write(f"[UPDT]    '{AppInfo.BuildType._value2member_map_[i].name.upper()}': S{srv[i]}:C{vc[i]}\r\n")
        if srv[i] > vc[i]:      # New version
            tc = (*tc, i)

    def _get_avs_and_bi(s: int, _j: Dict[str, Any]) -> Tuple[str, str]:
        avs = '4.%s' % '.'.join([(str(j) if i != s else str(srv[s])) for i, j in enumerate(vc)][::-1])
        bi = _j['r_%s' % {
            AppInfo.BuildType.STABLE.value: 'stbl',
            AppInfo.BuildType.BETA.value: 'beta',
            AppInfo.BuildType.ALPHA.value: 'alph'
        }[s]]['dc']

        return avs, bi

    match len(tc):
        case 0:
            # up to date
            return False, AppInfo.ConfigurationFile.config.BI, AppInfo.ConfigurationFile.config.AVS

        case 1:
            # One new stream
            avs, bi = _get_avs_and_bi(tc[0], j); del tc
            sys.stdout.write(f"[UPDT] Found new version {avs} ({bi}).\r\n")

            return True, bi, avs

        case 2 | 3:
            # Reduce the list of updates to 1: the latest release that complies with the stability restriction(s) set
            #       forth by the user in config.

            _all = [_get_avs_and_bi(tc[i], j) for i in tc]
            _avs, _bi = list(map(lambda l: l[0], _all)), list(map(lambda l: l[1], _all))
            _dc = list(map(lambda l: int(l.split('_')[1]), [b if b != '' else '_0_' for b in _bi]))

            avs, bi = {k: (a, b) for (k, a, b) in zip(_dc, _avs, _bi)}[max(*_dc)]

            # TODO: Make the above reduction more efficient/faster
            #   Importance: low (max 3 items to reduce)

            return True, bi, avs

        case _:
            sys.stderr.write(f"[WARN] Unexpected behaviour in updater (0x01: {len(tc)})\r\n")
            return False, AppInfo.ConfigurationFile.config.BI, AppInfo.ConfigurationFile.config.AVS
