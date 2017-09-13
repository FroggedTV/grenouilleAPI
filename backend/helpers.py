import requests
import base64

def UrlImageToBase64(url):
    response = requests.get(url)
    return base64.b64encode(response.content).decode('UTF-8')

