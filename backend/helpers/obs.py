import websocket
import json

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
