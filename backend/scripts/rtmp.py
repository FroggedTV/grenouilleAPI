#!/usr/bin/python3
import argparse

from grenouilleAPIClient.client import GrenouilleAPIClient

class RTMPScripts:

    def __init__(self, host, key):
        self.host = host
        self.key = key

    def process(self, action):
        try:
            function = getattr(self, action)
            if function is not None:
                function()
        except AttributeError as e:
            pass

    def publish_done(self):
        client = GrenouilleAPIClient(self.host, self.key)
        client.OBS_stop_record()
        client.OBS_change_scene('Waiting')

    def publish_start(self):
        client = GrenouilleAPIClient(self.host, self.key)
        client.OBS_change_scene('RTMP')
        client.OBS_start_record()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Script file to run on rtmp events.')
    parser.add_argument('--host', dest='host', default=None)
    parser.add_argument('--key', dest='key', default=None)
    parser.add_argument('--action', dest='action', default='')
    args = parser.parse_args()

    if args.host is None or args.key is None or args.action == '':
        print('No key or no action provided inside the script.')
        exit(0)

    engine = RTMPScripts(args.host, args.key)
    engine.process(args.action)
