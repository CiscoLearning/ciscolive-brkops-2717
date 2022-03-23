
from pprint import pprint
import json
import requests
from requests.auth import HTTPBasicAuth
import urllib3
import apis
import sys, getopt
import argparse

#Imports from Jinja2
from jinja2 import Environment, FileSystemLoader

#Import YAML from PyYAML
import yaml
from yaml.loader import SafeLoader



def main():
    # Workflow
    # Create template 
    # Version template (commit)
    # Deploy template 

    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="create OR update template", type=str, nargs=1)

    args = parser.parse_args()
    argument = vars(args)

    # Load data
    with open('data.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)

    #Load data from YAML file into Python dictionary
    config = yaml.safe_load(open('./configuration.yml'))

    #Load Jinja2 template
    env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('template.txt')

    #Render template using data and print the output
    template = template.render(config)

    if argument["action"][0].lower() == "create":
        project_name = data["template"]["projectName"]
        name_of_template = data["template"]["templateName"]
        tag_name = data["template"]["tag"]

        create_template_request = apis.create_template(name_of_template, project_name, template)
        if create_template_request[0] == 202:
            print("Status message: Template is being created")
            template_UUID = apis.get_template_UUID(name_of_template)
            create_template_request = apis.create_template_version(template_UUID)
        else: 
            print(create_template_request[0],create_template_request[2])

    elif argument["action"][0] == "update":
        None
    else:
        None

    # Load data
    with open('data.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)







    #Load data from YAML file into Python dictionary
    config = yaml.safe_load(open('./configuration.yml'))

    #Load Jinja2 template
    env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template('template.txt')

    #Render template using data and print the output
    template = template.render(config)


    #apis.create_template("testfrompython4", "CL22", template)

    return 

main()
