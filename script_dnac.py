#!/usr/bin/env python

"""
This script is used in order to create and provision configuration templates on Cisco DNA Center.

It is assumed that a separate YAML file with platform credentials and data has already been created.

The templates that are covered in this code are JINJA2.

"""
import argparse
from jinja2 import Environment, FileSystemLoader
import yaml
from yaml.loader import SafeLoader
import apis


def get_infra_data(filename):
    '''
    Load data regarding targeted DNA Center and template from an
    external file.
    '''
    with open(filename, encoding="utf8") as file:
        data = yaml.load(file, Loader=SafeLoader)
    return data

def get_parameters(filename):
    '''
    Load data from YAML file into Python dictionary
    '''
    with open(filename, encoding="utf8" ) as file:
        config = yaml.load(file, Loader=SafeLoader)
    return config

def collect_args():
    '''
    Collect and return the selected argument
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument("action", help="create OR update template", type=str, nargs=1)
    args = parser.parse_args()
    argument = vars(args)
    return argument

def create_config(parameters, template):
    '''
    Initialise Jinja2 environment and render the configuration.
    '''
    env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
    template = env.get_template(template)

    #Render template using data and print the output
    template = template.render(parameters)
    return template

def create_template(data,template):
    '''
    Create a new template in DNAC
    Commit version of the template in DNAC
    Deploy to device
    '''
    project_name = data["template"]["projectName"]
    name_of_template = data["template"]["templateName"]
    serial_number = data["host"]["serialNr"]

    create_template_request = apis.create_template(name_of_template, project_name, template)

    if create_template_request[0] == 202:
        print("Status message: Template is being created")
        template_uuid = apis.get_template_uuid(name_of_template)
        create_template_request = apis.create_template_version(template_uuid)

        choice = input("Do you want to proceed to deploy template to device? (yes/no)")
        if choice.lower() == ("yes" or "y"):
            apis.deployment_of_template(serial_number,name_of_template)
        else:
            print("Deployment of template aborted")

    else:
        print("Error message:")
        print(create_template_request[0],create_template_request[2])

def update_template(data, template):
    '''
    Update template
    '''
    project_name = data["template"]["projectName"]
    name_of_template = data["template"]["templateName"]
    serial_number = data["host"]["serialNr"]

    update_template_request = apis.update_template(project_name,name_of_template,template)
    if update_template_request[0] == 202:
        print("Status message: Template is being updated")
        template_uuid = apis.get_template_uuid(name_of_template)
        apis.create_template_version(template_uuid)
        choice = input("Do you want to proceed to deploy template to device? (yes/no)")
        if choice.lower() == ("yes" or "y"):
            apis.deployment_of_template(serial_number,name_of_template)
    else:
        print(update_template_request[0])

def main():
    """
    Main function that executes the following workflow:
    - open and parse data files: data.yaml and configuration.yaml
    - open JINJA2 template.txt
    - if argument is create: creates JINJA2 template in DNA Center
    - if argument is update: updates JINJA2 template in DNA Center
    - commit template in DNA Center
    - deploy template in DNA Center (optional)
    """
    data = get_infra_data("data.yaml")
    config = get_parameters("./configuration.yml")
    template = create_config(config, "template.txt")
    argument = collect_args()

    if argument["action"][0].lower() == "create":
        create_template(data, template)

    elif argument["action"][0].lower() == "update":
        update_template(data, template)


    else:
        print("ERROR: Do not recognize command. You can only choose create or update")

if __name__ == "__main__":
    main()
