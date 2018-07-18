import requests
import base64
import json
import logging

from models import GameVIPType

def safe_json_loads(string):
    """Loads a JSON or return empty JSON."""
    try:
        data = json.loads(string)
        return data
    except Exception as e:
        return {}

def url_image_to_base64(url):
    response = requests.get(url)
    return base64.b64encode(response.content).decode('UTF-8')

def divide_vip_list_per_type(vips):
    """Divide a list of GameVIPs into two lists containing casters and admins.

    Args:
        vips: list of GameVIPs
    Returns:
        admins: list of SteamIDs (64bits) from 'ADMIN' inside vips.
        casters: list of SteamIDs (64bits) from 'CASTER' inside vips.
    """
    admins = []
    casters = []

    for vip in vips:
        if vip['type'] == str(GameVIPType.ADMIN):
            admins.append(vip['id'])
        elif vip['type'] == str(GameVIPType.CASTER):
            casters.append(vip['id'])

    return admins, casters
