import yaml 
from yaml.loader import SafeLoader
import dnacentersdk
from pprint import pprint
import json
import requests
from requests.auth import HTTPBasicAuth
import urllib3

import apis

def main():
    
    token = apis.get_auth_token()
    
    return



