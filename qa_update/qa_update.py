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

import urllib3, sys, json
from typing import Optional, Callable, Any, Tuple, Dict, cast

from qa_std import AppInfo


URL = 'https://raw.githubusercontent.com/GeetanshGautam0/QAS4/release_%s/.conf/_BIH.json'
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


def check_for_updates(
    switch_build_type: Optional[AppInfo.BuildType] = None
) -> Tuple[bool, str]:
    global URL, HTTP

    if isinstance(switch_build_type, AppInfo.BuildType):
        bt = switch_build_type
    else:
        bt = AppInfo.ConfigurationFile.config.BT

    url = URL % bt.name.lower()

    sys.stdout.write(f'Trying to access {url} via the HTTP protocol ...\n')
    success, res = tr(  # type: ignore
        HTTP.request,   # type: ignore
        'GET',
        url,
        headers={'Cache-Control': 'no-cache', 'Pragma': 'no-cache', 'Expires': 'Thu, 01 Jan 1970 00:00:00 GMT'}
    )

    if not success:
        sys.stderr.write(f'[HTTP GET ERROR] Failed to access URL: {str(res)}')
        return False, AppInfo.ConfigurationFile.bih.BUILD_ID

    http_response = cast(urllib3.BaseHTTPResponse, res)
    if http_response.status != 200:
        sys.stderr.write(f'[HTTP GET ERROR] Failed to access URL: Status {http_response.status}')
        return False, AppInfo.ConfigurationFile.bih.BUILD_ID

    success, js = tr(json.loads, tr(http_response.data.decode)[1])  # type: ignore

    if not success:
        sys.stderr.write(f'[HTTP GET ERROR] Failed to access URL: JSON Decode Error')
        return False, AppInfo.ConfigurationFile.bih.BUILD_ID

    j = cast(Dict[str, Any], js)

    if j['arel'] > AppInfo.ConfigurationFile.bih.A_REL_N:
        sys.stdout.write(f'A new {bt.name} release of the app is available: {j["bid"]}\n')
        return True, j['bid']

    else:
        sys.stdout.write(f'NO new {bt.name} release of the app is available: {j["bid"]}\n')
        return False, AppInfo.ConfigurationFile.bih.BUILD_ID
