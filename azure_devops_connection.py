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
    REPOSITORIES = get_repository_list_from_repositories_json()


def get_json_from_api():
    return requests.get(API_URL, auth=(USERNAME, PERSONAL_ACCESS_TOKEN)).json()['value']


def get_repository_list_from_repositories_json():
    repositories = []
    for element in REPOSITORIES_JSON:
        repositories.append(element['name'])
    return repositories


def get_repository_from_repositories_json(repository_name):
    repository = None
    for element in REPOSITORIES_JSON:
        if repository_name.lower() == element['name'].lower():
            repository = element
    return repository


def print_repository_list():
    print(*sorted(REPOSITORIES), sep=', ')


def get_repository_info(repository_name):
    repository = get_repository_from_repositories_json(repository_name)
    repository_infos = []

    if repository != None:
        repository_infos.append('Name: ' + repository['name'])
        repository_infos.append('Project: ' + repository['project']['name'])
        repository_infos.append('Size: ' + size(repository['size']))
        repository_infos.append('Remote URL: ' + repository['remoteUrl'])
        repository_infos.append('SSH URL: ' + repository['sshUrl'])
        repository_infos.append('Web URL: ' + repository['webUrl'])
    else:
        repository_infos.append('Nothing found')

    print(*repository_infos, sep='\n')


def open_repository(repository_name):
    webbrowser.open_new(GIT_URL + repository_name)


def create_repository(repository_name):
    try:
        response = requests.post(API_URL, json={"name": repository_name}, auth=(
            USERNAME, PERSONAL_ACCESS_TOKEN))
        response.raise_for_status()
        print("Repositoy created successfully")
    except requests.exceptions.HTTPError:
        print("Error " + str(response.status_code) + ": " + response.reason)
