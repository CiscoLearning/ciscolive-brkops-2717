#!/usr/bin/env python

"""
This script is used in order to create and provision configuration templates on Cisco DNA Center.

It is assumed that a separate YAML file with platform credentials and data has already been created.

The templates that are covered in this code are JINJA2.

"""
from jinja2 import Environment, FileSystemLoader
import yaml
from yaml.loader import SafeLoader
import apis
from apis import data, configuration


# Load data
with open('data.yaml', encoding="utf8") as f:
    data = yaml.load(f, Loader=SafeLoader)

#Load data from YAML file into Python dictionary
with open('./configuration.yml', encoding="utf8" ) as c:
    config = yaml.load(c, Loader=SafeLoader)

#config = yaml.safe_load(open('./configuration.yml'))

#Load Jinja2 template
env = Environment(loader = FileSystemLoader('./'), trim_blocks=True, lstrip_blocks=True)
template = env.get_template('template.txt')

#Render template using data and print the output
template = template.render(config)

def main():
    """
    Main function that executes the following workflow:
    - open and parse data files: data.yaml and configuration.yaml
    - open JINJA2 template.txt
    - commit template in DNA Center
    - deploy template in DNA Center (optional)
    """
    name_of_template = data["template"]["templateName"]
    serial_number = data["host"]["serialNr"]
    project_name = data["template"]["projectName"]

    template_uuid = apis.get_template_uuid(name_of_template)

    if template_uuid is None:
        print("\nERROR:")
        print("Template doesn't exist and needs to be created \n\n")

    else:
        print("\nTemplate exists and will be deployed\n\n")

        deploy = apis.deployment_of_template(serial_number,name_of_template)
        task_id = deploy[1]

        if task_id is None:
            print(f"ERROR: {deploy[2]}")
        else:
            task_status = apis.get_task_status(task_id)

            if "Successfully" in task_status:
                print(f"\nTask stats: \"{task_status}\" and task_id: {task_id}")

                # Go ahead and commit the template
                template_uuid = apis.get_template_uuid(name_of_template)
                commit = apis.create_template_version(template_uuid)
                task_id = commit[1]
                task_status = apis.get_task_status(task_id)
                if "Successfully" in task_status:
                    print(f"\nTask stats: \"{task_status}\" and task_id: {task_id}")
            else:
                print(f"\nTask stats: \"{task_status}\" and task_id: {task_id}")


if __name__ == "__main__":
    main()
    