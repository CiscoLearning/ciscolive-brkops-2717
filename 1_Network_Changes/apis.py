#!/usr/bin/env python
"""
This script is used in order to define all API calls that are needed in script_dnac.py

It is assumed that a separate YAML files with credentials and data has already been created.

The templates that are covered in this code are JINJA2.

"""
from pprint import pprint
import yaml
from yaml.loader import SafeLoader
import requests
import urllib3

urllib3.disable_warnings()

# Load data file
with open("data.yaml", encoding="utf8") as d:
    data = yaml.load(d, Loader=SafeLoader)

# Load configuration file
with open("configuration.yml", encoding="utf8") as c:
    configuration = yaml.load(c, Loader=SafeLoader)

BASE_URL = f"https://{data['dnac']['url']}"

def get_auth_token():
    """
    Building out Auth request. Using requests.post to make a call to the Auth Endpoint
    """
    url = f"{BASE_URL}/dna/system/api/v1/auth/token"
    resp = requests.post(
        url,
        auth=(data["dnac"]["username"], data["dnac"]["password"]),
        verify=False,
    )
    token = resp.json()["Token"]
    return token

def get_tag_id(tag_name):
    """
    Function retrieves the tag ID
    """
    url = f"{BASE_URL}/dna/intent/api/v1/tag?name={tag_name}"
    headers = {"Content-Type": "application/json", "X-Auth-Token": get_auth_token()}
    response = requests.get(url=url, headers=headers, verify=False)
    if response.status_code == 200:
        response_data = response.json()
        tag_id = response_data["response"][0]["id"]
    else:
        print(response.status_code)
    return tag_id

def get_project_data(project_name):
    """
    Function retrieves project data
    """
    url = f"{BASE_URL}/dna/intent/api/v1/template-programmer/project?name={project_name}"

    headers = {"Content-Type": "application/json", "X-Auth-Token": get_auth_token()}

    response = requests.get(url=url, headers=headers, verify=False)

    if response.status_code == 200:
        response_data = response.json()
    else:
        print(response.status_code)
        pprint(response.json())

    return response_data

def create_template(name_of_template, project_name, template):
    """
    Function creates a template in a given project
    """
    project_data = get_project_data(project_name)
    project_uuid = project_data[0]["id"]
    #tag_name = data["template"]["tag"]

    url = f"{BASE_URL}/dna/intent/api/v1/template-programmer/project/{project_uuid}/template"

    headers = {"Content-Type": "application/json", "X-Auth-Token": get_auth_token()}

    params = [
        {"parameterName": "vlans", "dataType": "STRING", "required": True, "order": 1}
    ]

    payload = {
        #"tags": [{"name": tag_name, "id": get_tag_id(tag_name)}],
        "deviceTypes": [
            {
                "productFamily": "Switches and Hubs",
            }
        ],
        "failurePolicy": "ABORT_ON_ERROR",
        "language": "JINJA",
        "name": name_of_template,
        "templateContent": template,
        "projectName": project_name,
        "softwareType": "IOS-XE",
        "templateParams": params,
    }

    response = requests.post(
        url=url, headers=headers, json=payload, verify=False
    )

    if response.status_code == 202:
        response_data = response.json()
        task_id = response_data["response"]["taskId"]
        response_message = ""
    else:
        task_id = ""
        response_data = response.json()
        response_message = response_data["response"]["message"]
    return response.status_code, task_id, response_message


def get_template_uuid(name_of_template):
    """
    Function retrieves an existing template´s UUID
    """
    project_data = get_project_data("CL22")
    for item in project_data:
        if item["name"] == "CL22":
            templates = item["templates"]
            for item_2 in templates:
                if item_2["name"] == str(name_of_template):
                    template_uuid = item_2["id"]
                else:
                    template_uuid = None
    return template_uuid


def get_device_uuid_by_serial(serial_number):
    """
    Function retrieves device UUID by serial number
    """
    url = f"{BASE_URL}/dna/intent/api/v1/network-device/serial-number/{serial_number}"
    headers = {"Content-Type": "application/json", "X-Auth-Token": get_auth_token()}
    response = requests.get(url=url, headers=headers, verify=False)
    response_data = response.json()
    device_uuid = response_data["response"]["id"]
    return device_uuid


def update_template(project_name, name_of_template, template):
    """
    Function updates a template with new data
    """
    template_uuid = get_template_uuid(name_of_template)
    software_type = data["host"]["platform"].upper()

    url = f"{BASE_URL}/dna/intent/api/v1/template-programmer/template"
    headers = {"Content-Type": "application/json", "X-Auth-Token": get_auth_token()}

    payload = {
        "deviceTypes": [{"productFamily": "Switches and Hubs"}],
        "language": "JINJA",
        "name": name_of_template,
        "projectName": project_name,
        "softwareType": software_type,
        "templateContent": template,
        "id": template_uuid,
    }

    response = requests.put(
        url=url, headers=headers, verify=False, json=payload
    )

    if response.status_code == 202:
        response_data = response.json()
        task_id = response_data["response"]["taskId"]
        response_message = ""
    else:
        task_id = ""
        response_data = response.json()
        response_message = response_data["response"]["message"]
    return response.status_code, task_id, response_message

def create_template_version(template_uuid):
    """
    Function commits a created template by committing it
    """
    url = f"{BASE_URL}/dna/intent/api/v1/template-programmer/template/version"
    headers = {"Content-Type": "application/json", "X-Auth-Token": get_auth_token()}

    payload = {"comments": "test from Python", "templateId": template_uuid}

    response = requests.post(
        url=url, headers=headers, verify=False, json=payload
    )

    if response.status_code == 202:
        response_data = response.json()
        task_id = response_data["response"]["taskId"]
        response_message = None
    else:
        task_id = None
        response_data = response.json()
        response_message = response_data["response"]["message"]
    return response.status_code, task_id, response_message


def deployment_of_template(serial_number, name_of_template):
    """
    Function deploys a template based on template name
    """
    url = f"{BASE_URL}/dna/intent/api/v2/template-programmer/template/deploy"
    # print(parameters)
    headers = {"Content-Type": "application/json", "X-Auth-Token": get_auth_token()}

    template_uuid = get_template_uuid(name_of_template)
    device_uuid = get_device_uuid_by_serial(serial_number)

    payload = {
        "targetInfo": [
            {
                "id": device_uuid,
                "type": "MANAGED_DEVICE_UUID",
                "versionedTemplateId": template_uuid
                # "params": parameters,
            }
        ],
        "templateId": template_uuid,
    }

    response = requests.post(
        url=url, headers=headers, json=payload, verify=False
    )

    if response.status_code == 202:
        response_data = response.json()
        task_id = response_data["response"]["taskId"]
        response_message = None
    else:
        task_id = None
        response_data = response.json()
        response_message = response_data["response"]["message"]
    return response.status_code, task_id, response_message

def get_task_status(task_id):
    """
    Function retrieves status data of a specific task
    """
    print(task_id)
    url = f"{BASE_URL}/dna/intent/api/v1/task/{task_id}"
    headers = {"Content-Type": "application/json", "X-Auth-Token": get_auth_token()}

    response = requests.get(url=url, headers=headers, verify=False)

    if response.status_code == 200:
        response_data = response.json()
        task_status = response_data["response"]["progress"]
    return task_status


def delete_template(name_of_template):
    """
    Function deletes an existing template
    """
    template_id = get_template_uuid(name_of_template)
    url = f"{BASE_URL}/dna/intent/api/v1/template-programmer/template/{template_id}"
    headers = {"Content-Type": "application/json", "X-Auth-Token": get_auth_token()}

    response = requests.delete(url=url, headers=headers, verify=False)

    if response.status_code == 200:
        response_data = response.json()

    return response.status_code, response_data


if __name__ == "__main__":
    print("This script defines the API calls that are used when executing script_dnac.py")
