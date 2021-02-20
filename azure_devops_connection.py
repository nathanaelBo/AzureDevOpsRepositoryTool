import configparser
import requests
import webbrowser
from hurry.filesize import size


class AzureDevOpsConnection():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('config.ini')

        self.USERNAME = config.get('Credentials', 'USERNAME')
        self.PERSONAL_ACCESS_TOKEN = config.get(
            'Credentials', 'PERSONAL_ACCESS_TOKEN')

        self.API_URL = config.get('AzureDevOps', 'API_URL')
        self.GIT_URL = config.get('AzureDevOps', 'GIT_URL')

        self.REPOSITORIES_JSON = self.get_json_from_api()
        self.REPOSITORIES = self.get_repository_list_from_repositories_json()

    def get_json_from_api(self):
        return requests.get(self.API_URL, auth=(self.USERNAME, self.PERSONAL_ACCESS_TOKEN)).json()['value']

    def get_repository_list_from_repositories_json(self):
        repositories = []
        for element in self.REPOSITORIES_JSON:
            repositories.append(element['name'])
        return repositories

    def get_repository_from_repositories_json(self, repository_name):
        repository = None
        for element in self.REPOSITORIES_JSON:
            if repository_name.lower() == element['name'].lower():
                repository = element
        return repository

    def print_repository_list(self):
        print(*sorted(self.REPOSITORIES), sep=', ')

    def get_repository_info(self, repository_name):
        repository = self.get_repository_from_repositories_json(
            repository_name)
        repository_infos = []

        if repository != None:
            repository_infos.append('Name: ' + repository['name'])
            repository_infos.append(
                'Project: ' + repository['project']['name'])
            repository_infos.append('Size: ' + size(repository['size']))
            repository_infos.append('Remote URL: ' + repository['remoteUrl'])
            repository_infos.append('SSH URL: ' + repository['sshUrl'])
            repository_infos.append('Web URL: ' + repository['webUrl'])
        else:
            repository_infos.append('Nothing found')

        print(*repository_infos, sep='\n')

    def open_repository(self, repository_name):
        webbrowser.open_new(self.GIT_URL + repository_name)

    def create_repository(self, repository_name):
        try:
            response = requests.post(self.API_URL, json={"name": repository_name}, auth=(
                self.USERNAME, self.PERSONAL_ACCESS_TOKEN))
            response.raise_for_status()
            print("Repositoy created successfully")
        except requests.exceptions.HTTPError:
            print("Error " + str(response.status_code) + ": " + response.reason)
