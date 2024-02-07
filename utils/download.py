import requests
import cbor
import time

from utils.response import Response

def download(url, config, logger=None):
    if config.cache_server is None:
        raise ValueError("Cache server details are not set in config.")
    host, port = config.cache_server
    # print(f"Downloading {url} using cache {host}:{port}")
    req_args={
        'url' : f"http://{host}:{port}/",
        'params' : [("q", f"{url}"), ("u", f"{config.user_agent}")]
    }
    # print(req_args)
    resp = requests.get(**req_args, timeout=5)
    try:
        if resp and resp.content:
            a = Response(cbor.loads(resp.content))
            # print(a)
            return a
    except (EOFError, ValueError) as e:
        pass
    logger.error(f"Spacetime Response error {resp} with url {url}.")
    return Response({
        "error": f"Spacetime Response error {resp} with url {url}.",
        "status": resp.status_code,
        "url": url})
