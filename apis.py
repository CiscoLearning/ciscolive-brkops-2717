import yaml 
from yaml.loader import SafeLoader
import dnacentersdk
from pprint import pprint
import json
import requests
from requests.auth import HTTPBasicAuth
import urllib3

urllib3.disable_warnings()

# Load data
with open('data.yaml') as f:
    data = yaml.load(f, Loader=SafeLoader)


# Load configuration
with open('configuration.yml') as f:
    configuration= yaml.load(f, Loader=SafeLoader)

BASE_URL = "https://{}".format(data["credentials"]["dnac"]["url"])  

# Get authentication token
def get_auth_token():
    """
    Building out Auth request. Using requests.post to make a call to the Auth Endpoint
    """
    url = BASE_URL + '/dna/system/api/v1/auth/token'    
    resp = requests.post(url, auth=HTTPBasicAuth(data["credentials"]["dnac"]["username"], data["credentials"]["dnac"]["password"]), verify=False)  # Make the POST Request
    token = resp.json()['Token']     
    return token    

# Get TAGID

def get_tagID(tag_name):
    url = BASE_URL + "/dna/intent/api/v1/tag?name=" + str(tag_name)
    headers = {
        "Content-Type" : "application/json",
        "X-Auth-Token" : get_auth_token()
    }
    response = requests.get(url=url, headers=headers, verify=False)

    if response.status_code == 200:
        responseData = response.json()
        tagID = responseData["response"][0]["id"]
    else: 
        print(response.status_code)

    return tagID

# Create project
def create_project():
    url = BASE_URL + "/dna/intent/api/v1/template-programmer/project"
    headers = {
        "Content-Type" : "application/json",
        "X-Auth-Token" : get_auth_token()
    }

    payload = {
        
        "tags": [
            {
                "id": "string",
                "name": "string"
            }
        ],
        "createTime": "integer",
        "description": "string",
        "id": "string",
        "lastUpdateTime": "integer",
        "name": "string",
        "templates": "any"

    }

    response = requests.post(url=url, headers=headers, verify=False)

    if response.status_code == 200:
        responseData = response.json()
        pprint(responseData)
    return

# Get project 
def get_project_data(project_name):
    url= BASE_URL + "/dna/intent/api/v1/template-programmer/project?name=" + str(project_name)

    headers = {
        "Content-Type" : "application/json",
        "X-Auth-Token" : get_auth_token()
    }

    response = requests.get(url=url, headers=headers, verify=False)

    if response.status_code == 200:
        responseData = response.json()
    else:
        print(response.status_code)
        pprint(response.json())

    return responseData


def create_template(name_of_template, project_name, template):

    project_data = get_project_data(project_name)
    projectUUID = project_data[0]["id"]
    tagName = data["template"]["tag"]

    url = BASE_URL + "/dna/intent/api/v1/template-programmer/project/{}/template".format(projectUUID)

    headers = {
        "Content-Type" : "application/json",
        "X-Auth-Token" : get_auth_token()
    }
    payload = {
        "tags": [
            {
                "name": tagName,
                "id" : get_tagID(tagName)
            }
         ],

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

        }
    
    response = requests.post(url=url, headers=headers, data=json.dumps(payload), verify=False)

    if response.status_code == 202: 
        responseData = response.json()
        taskID = responseData["response"]["taskId"]
        responseMessage = ""
    else: 
        taskID = ""
        responseData = response.json()
        responseMessage = responseData["response"]["message"]
    return response.status_code, taskID, responseMessage


def get_template_uuid(name_of_template):
    projectsData = get_project_data("CL22")
    for item in projectsData:
        if item["name"] == "CL22":
            templates = item["templates"]
            for item in templates:
                if item["name"] == str(name_of_template):
                    template_uuid = item["id"]
                else: 
                    template_uuid = None
    return template_uuid


def get_deviceUUID_by_serial(serial_number):

    url = BASE_URL + "/dna/intent/api/v1/network-device/serial-number/" + serial_number
    headers = {
        "Content-Type" : "application/json",
        "X-Auth-Token" : get_auth_token()
    }   
    resp = requests.get(url=url, headers=headers, verify=False)
    data = resp.json()
    device_UUID = data["response"]["id"]
    return device_UUID



def update_template(project_name, name_of_template,template):
    with open('data.yaml') as f:
        data = yaml.load(f, Loader=SafeLoader)
    project_data = get_project_data(project_name)
    projectUUID = project_data[0]["id"]
    tagName = data["template"]["tag"]
    template_uuid = get_template_uuid(name_of_template)
    softwareType = data["host"]["platform"].upper()

    url = BASE_URL + "/dna/intent/api/v1/template-programmer/template"
    headers = {
        "Content-Type" : "application/json",
        "X-Auth-Token" : get_auth_token()
    }     

    payload = {

        "deviceTypes": [
            {
                "productFamily": "Switches and Hubs"
            }
        ],
        "language": "JINJA",
        "name": name_of_template,
        "projectName": project_name,
        "softwareType": softwareType,
        "templateContent": template,
        "id" : template_uuid
        
    }


    response = requests.put(url=url, headers=headers, verify=False, data= json.dumps(payload))

    if response.status_code == 202: 
        responseData = response.json()
        taskID = responseData["response"]["taskId"]
    else: 
        taskID = ""
        responseData = response.json()
        responseMessage = responseData["response"]["message"]
    return response.status_code, taskID, responseMessage


# COMMIT TEMPLATE VERSION
def create_template_version(template_uuid):
    url = BASE_URL + "/dna/intent/api/v1/template-programmer/template/version"
    headers = {
        "Content-Type" : "application/json",
        "X-Auth-Token" : get_auth_token()
    }

    payload = {
        "comments" : "test from Python",
        "templateId" : template_uuid
    }

    response = requests.post(url=url, headers=headers, verify=False, data= json.dumps(payload))

    if response.status_code == 202: 
        responseData = response.json()
        taskID = responseData["response"]["taskId"]
        responseMessage = None
    else: 
        taskID = None
        responseData = response.json()
        responseMessage = responseData["response"]["message"]
    return response.status_code, taskID, responseMessage

def get_template_version_ID(name_of_template,version):
    template_uuid = get_template_uuid(name_of_template)
    url = BASE_URL + "/dna/intent/api/v1/template-programmer/template/version/" + template_uuid
    headers = {
        "Content-Type" : "application/json",
        "X-Auth-Token" : token
    }

    resp = requests.get(url = url, headers=headers, verify = False)

    if resp.status_code == 200:
        responseData = resp.json()
        versionsInfo_list = responseData[0]["versionsInfo"]
        versionsInfo_list.pop(0)

        if version == "latest":
            version_number = len(versionsInfo_list)

            for item in versionsInfo_list:
                if item["version"] == str(version_number):
                    versionID = item["id"]
                    print(versionID)
                    break

        else:
            version_number = version

            for item in versionsInfo_list:
                if item["version"] == str(version_number):
                    versionID = item["id"]
                    print(versionID)
                    break             

    else:
        pprint(response.json())

    return versionID

def deployment_of_template(serial_number, name_of_template):
    url = BASE_URL + "/dna/intent/api/v2/template-programmer/template/deploy"

    headers = {
        "Content-Type" : "application/json",
        "X-Auth-Token" : get_auth_token()
    }

    template_uuid = get_template_uuid(name_of_template)
    TEMPLATE_VERSION_UUID = "test"
    DEVICE_UUID = get_deviceUUID_by_serial(serial_number)

    Data = {
        "targetInfo" : [
            {
                "id" : DEVICE_UUID,
                "type" : "MANAGED_DEVICE_UUID",
                "versionedTemplateId": template_uuid
            }
        ],
        "templateId" : template_uuid

    }

    response = requests.post(url=url, headers=headers, data=json.dumps(Data), verify=False)
    
    if response.status_code == 202: 
        responseData = response.json()
        taskID = responseData["response"]["taskId"]
        responseMessage = None
    else: 
        taskID = None
        responseData = response.json()
        responseMessage = responseData["response"]["message"]
    return response.status_code, taskID, responseMessage


# GET TASK STATUS
def get_task_status(taskID):
    print(taskID)
    url = BASE_URL + "/dna/intent/api/v1/task/" + taskID
    headers={
        "Content-Type" : "application/json",
        "X-Auth-Token" : get_auth_token()
    }

    response = requests.get(url =url, headers=headers, verify=False)


    if response.status_code == 200:
        responseData = response.json()
        task_status = responseData["response"]["progress"]
    return task_status

def delete_template(name_of_template):
    templateId = get_template_uuid(name_of_template)
    url = BASE_URL + f"/dna/intent/api/v1/template-programmer/template/{templateId}"
    headers={
        "Content-Type" : "application/json",
        "X-Auth-Token" : get_auth_token()
    }

    response = requests.delete(url =url, headers=headers, verify=False)

    if response.status_code == 200:
        responseData = response.json()
        #task_status = responseData["response"]["progress"]

    return response.status_code



if __name__ == "__main__":

    name_of_template = data["template"]["templateName"]
    template_uuid = get_template_uuid(name_of_template)
    create_template_version(template_uuid)