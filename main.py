import argparse
from azure_devops_connection import AzureDevOpsConnection
import sys


class AzureDevOpsRepositoryTool():
    def __init__(self):
        self.azure_devops_connection = AzureDevOpsConnection()

        parser = argparse.ArgumentParser(
            description='Helper Tool for Azure DevOps Repositories')
        parser.add_argument('command', help='Subcommand to run')
        args = parser.parse_args(sys.argv[1:2])

        if not hasattr(self, args.command):
            print('Unrecognized command')
            parser.print_help()
            exit(1)

        getattr(self, args.command)()

    def open(self):
        parser = argparse.ArgumentParser(
            description='Opens an Azure DevOps Repository in your default browser')
        parser.add_argument(
            'repository', choices=self.azure_devops_connection.REPOSITORIES)
        args = parser.parse_args(sys.argv[2:])

        self.azure_devops_connection.open_repository(args.repository)

    def info(self):
        parser = argparse.ArgumentParser(
            description='Shows information about an Azure DevOps Repository')
        parser.add_argument(
            'repository', choices=self.azure_devops_connection.REPOSITORIES)
        args = parser.parse_args(sys.argv[2:])

        self.azure_devops_connection.get_repository_info(args.repository)

    def create(self):
        parser = argparse.ArgumentParser(
            description='Creates a new Azure DevOps Repository')
        parser.add_argument('repository')
        args = parser.parse_args(sys.argv[2:])

        self.azure_devops_connection.create_repository(args.repository)

    def list(self):
        parser = argparse.ArgumentParser(
            description='Lists all existing Azure DevOps Repositories')
        self.azure_devops_connection.print_repository_list()


if __name__ == '__main__':
    AzureDevOpsRepositoryTool()
