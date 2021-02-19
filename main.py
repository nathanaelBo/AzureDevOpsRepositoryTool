import argparse
import azure_devops_connection


def main():
    azure_devops_connection.init()

    parser = argparse.ArgumentParser(description='Helper Tool for Azure DevOps Repositories')

    parser.add_argument('-o', '--open', type=str, required=False, dest='open_repository', action='store',
                        choices=azure_devops_connection.REPOSITORIES, help='Opens an Azure DevOps Repository in your default browser')
    parser.add_argument('-i', '--info', type=str, required=False,
                        dest='get_repository_info', action='store', choices=azure_devops_connection.REPOSITORIES,
                        help='Shows information about an Azure DevOps Repository')
    parser.add_argument('-c', '--create', type=str, required=False,
                        dest='create_repository', action='store',
                        help='Creates a new Azure DevOps Repository')
    parser.add_argument('-l', '--list', required=False,
                        dest='show_repository_list', action='store_true',
                        help='Lists all existing Azure DevOps Repositories')

    args = parser.parse_args()

    if args.open_repository:
        azure_devops_connection.open_repository(args.open_repository)
    elif args.get_repository_info:
        azure_devops_connection.get_repository_info(args.get_repository_info)
    elif args.create_repository:
        azure_devops_connection.create_repository(args.create_repository)
    elif args.show_repository_list:
        azure_devops_connection.print_repository_list()
    else:
        return


if __name__ == '__main__':
    main()
