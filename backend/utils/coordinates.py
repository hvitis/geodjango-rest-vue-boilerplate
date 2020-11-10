import sys
import urllib.request
import json
from django.conf import settings

def get_lat_lng_from_ip(ip_address):
    """Returns array that consists of latitude and longitude"""
    URL = 'https://ipinfo.io/{}?token={}'.format(ip_address, settings.IPINFO_ACCESS_TOKEN)
    try:
        result = urllib.request.urlopen(URL).read()
        result = json.loads(result)
        result = result['loc']
        lat, lng = result.split(',')
        return [lat, lng]
    except:
        print("Could not load: ", URL)
        return [None, None]