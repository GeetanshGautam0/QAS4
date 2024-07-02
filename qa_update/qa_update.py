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
from typing import Optional, Callable, Any, Tuple, Dict, cast

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


def check_for_updates() -> Tuple[bool, str]:
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
        return False, AppInfo.ConfigurationFile.config.BI

    http_response = cast(urllib3.BaseHTTPResponse, res)
    if http_response.status != 200:
        sys.stderr.write(f'[HTTP GET ERROR] Failed to access URL: Status {http_response.status}')
        return False, AppInfo.ConfigurationFile.config.BI

    success, js = tr(json.loads, tr(http_response.data.decode)[1])  # type: ignore

    if not success:
        sys.stderr.write(f'[HTTP GET ERROR] Failed to access URL: JSON Decode Error')
        return False, AppInfo.ConfigurationFile.config.BI

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

        return False, AppInfo.ConfigurationFile.config.BI         # Cannot update app so we can return.

    # else:

    # TODO
    #       Once an update stream is set, use the information to check
    #       arel, brel, and/or srel

    # Load the date codes of arel, brel, and srel.
    # An update is available if an update is issued to the selected "stream" or a more stable stream.

    bl = AppInfo.ConfigurationFile.config.AVS.split('.')
    assert bl.pop(0) == '4'  # Make sure that this configuration is for the 4th version of the app
    assert len(bl) == 3      # Version info

    vc = map(lambda x: int(x), bl)  # S, B, A
    pop = AppInfo.ConfigurationFile.config.BT.value  # Items to pop

    for i in range(3 - pop):
        print(srv[i])
