
from pprint import pprint
import json
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import apis

#Imports from Jinja2
from jinja2 import Environment, FileSystemLoader

#Import YAML from PyYAML
import yaml
from yaml.loader import SafeLoader



def main():

    #Load data from YAML file into Python dictionary
    config = yaml.safe_load(open('./configuration.yml'))

    #Load Jinja2 template
    env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('template.txt')

    #Render template using data and print the output
    template = template.render(config)

    apis.create_template("testfrompython4", "CL22", template)

    return 

main()
