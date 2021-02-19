import configparser
import requests
import webbrowser
from hurry.filesize import size


def init():
    global config
    config = configparser.ConfigParser()
    config.read('config.ini')

    global USERNAME
    USERNAME = config.get('Credentials', 'USERNAME')

    global PERSONAL_ACCESS_TOKEN
    PERSONAL_ACCESS_TOKEN = config.get('Credentials', 'PERSONAL_ACCESS_TOKEN')

    global API_URL
    API_URL = config.get('AzureDevOps', 'API_URL')

    global GIT_URL
    GIT_URL = config.get('AzureDevOps', 'GIT_URL')

    global REPOSITORIES_JSON
    REPOSITORIES_JSON = get_json_from_api()

    global REPOSITORIES
    REPOSITORIES = get_repository_list_from_json(REPOSITORIES_JSON)


def get_json_from_api():
    return requests.get(API_URL, auth=(USERNAME, PERSONAL_ACCESS_TOKEN)).json()['value']


def get_repository_list_from_json(json):
    repositories = []
    for element in json:
        repositories.append(element['name'])
    return repositories


def print_repository_list():
    print(*REPOSITORIES, sep=', ')


def get_repository_info(repository_name):
    repository = None
    repository_infos = []

    for element in REPOSITORIES_JSON:
        if repository_name.lower() == element['name'].lower():
            repository = element

    if repository != None:
        repository_infos.append('Name: ' + repository['name'])
        repository_infos.append('Project: ' + repository['project']['name'])
        repository_infos.append('Size: ' + size(repository['size']))
        repository_infos.append('Remote URL: ' + repository['remoteUrl'])
        repository_infos.append('SSH URL: ' + repository['sshUrl'])
        repository_infos.append('Web URL: ' + repository['webUrl'])
    else:
        repository_infos = 'Nothing found'

    print(*repository_infos, sep='\n')


def open_repository(repository_name):
    webbrowser.open_new(GIT_URL + repository_name)
