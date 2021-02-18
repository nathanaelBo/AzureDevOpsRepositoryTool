import base64
import configparser
import requests
import webbrowser
from hurry.filesize import size

def init():
    global config
    config = configparser.ConfigParser()
    config.read('config.ini')

    global USERNAME
    USERNAME = config.get('Credentials','USERNAME')

    global PERSONAL_ACCESS_TOKEN
    PERSONAL_ACCESS_TOKEN = config.get('Credentials','PERSONAL_ACCESS_TOKEN')

    global API_URL
    API_URL = config.get('AzureDevOps','API_URL')

    global GIT_URL
    GIT_URL = config.get('AzureDevOps','GIT_URL')

    global REPOS_JSON
    REPOS_JSON = get_json_from_api()

    global REPOS
    REPOS = get_repo_list_from_json(REPOS_JSON)

def get_authorization_header():
    authorization_string = USERNAME + ':' + PERSONAL_ACCESS_TOKEN
    base64_authorization_string = base64.b64encode(authorization_string.encode()).decode()
    return {'Authorization': 'Basic %s' % base64_authorization_string}

def get_json_from_api():
    authorization_header = get_authorization_header()
    return requests.get(API_URL, headers=authorization_header).json()['value']

def get_repo_list_from_json(json):
    repos = []
    for element in json:
        repos.append(element['name'])
    return repos

def print_repo_list():
    print(*REPOS, sep=', ')


def get_repo_info(repo_name):
    repo = None
    repo_infos = []

    for element in REPOS_JSON:
        if repo_name.lower() == element['name'].lower():
            repo = element

    if repo != None:
        repo_infos.append('Name: ' + repo['name'])
        repo_infos.append('Project: ' + repo['project']['name'])
        repo_infos.append('Size: ' + size(repo['size']))
        repo_infos.append('Remote URL: ' + repo['remoteUrl'])
        repo_infos.append('SSH URL: ' + repo['sshUrl'])
        repo_infos.append('Web URL: ' + repo['webUrl'])
    else:
        repo_infos = 'Nothing found'

    print(*repo_infos, sep='\n')

def open_repo(repo_name):
    webbrowser.open_new(GIT_URL + repo_name)
