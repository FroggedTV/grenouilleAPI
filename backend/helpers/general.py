import requests
import base64
import json
import logging
from datetime import datetime, timedelta
from apiclient import discovery

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

def get_calendar_events(google_api_key, calendar_id):
    calendar_events = [[], []]
    start_datetime = [datetime.now(), datetime.now()]
    end_datetime = [datetime.now(), datetime.now()]
    start_datetime[0] = start_datetime[0] - timedelta(days=start_datetime[0].weekday(),
                                                      hours=start_datetime[0].hour,
                                                      minutes=start_datetime[0].minute,
                                                      seconds=start_datetime[0].second,
                                                      microseconds=start_datetime[0].microsecond)

    start_datetime[1] = start_datetime[0] + timedelta(days=7)
    end_datetime[0] = start_datetime[0] + timedelta(days=7)
    end_datetime[1] = start_datetime[1] + timedelta(days=7)

    try:
        service = discovery.build('calendar', 'v3',
                                  developerKey=google_api_key,
                                  cache_discovery=False)

        for i in range(0, 2):
            events_result = service.events().list(calendarId=calendar_id,
                                                  timeMin=start_datetime[i].isoformat() + 'Z',
                                                  maxResults=40,
                                                  singleEvents=True,
                                                  orderBy='startTime').execute()
            events = events_result.get('items', [])

            for event in events:
                if 'dateTime' not in event['start'] or 'dateTime' not in event['end']:
                    continue
                start = event['start'].get('dateTime')
                start = datetime.strptime(''.join(start.rsplit(':', 1))[:18],
                                          "%Y-%m-%dT%H:%M:%S")
                start.replace(tzinfo=None)
                if start > end_datetime[i]:
                    continue
                end = event['end'].get('dateTime')
                end = datetime.strptime(''.join(end.rsplit(':', 1))[:18],
                                        "%Y-%m-%dT%H:%M:%S")
                if start.hour < 10:
                    start = start.replace(hour=10, minute=0, second=0)
                if end > end_datetime[i]:
                    end = end_datetime[i]
                title = event['summary']
                calendar_events[i].append({'start': start, 'end': end, 'title': title})
        return calendar_events
    except Exception as e:
        logging.exception(e)
        return None