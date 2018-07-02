import requests
import base64
import json
import websocket

from models import GameVIPType

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

def send_command_to_obs(command, options):
    """Send a command to obs through the WebSocket.

    Args:
        command: String command to send to OBS.
        options: JSON options added to the command.
    Returns:
        JSON Answer from the WebSocket.
    """
    ws = websocket.WebSocket()
    ws.connect("ws://{}:{}".format('127.0.0.1', '4444'))

    payload = options
    payload['message-id'] = 1
    payload['request-type'] = command

    ws.send(json.dumps(payload))
    result = json.loads(ws.recv())
    ws.close()

    return result
