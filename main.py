import argparse
import azure_devops_connection

def main():
    azure_devops_connection.init()

    parser = argparse.ArgumentParser(description='Open Azure DevOps Git Repo')

    parser.add_argument('-o', '--open', type=str, required=False, dest='open_repository', action='store', choices=azure_devops_connection.REPOSITORIES, help='Öffnet ein Azure DevOps Repository im Browser')
    parser.add_argument('-i', '--info', type=str, required=False,
                        dest='get_repository_info', action='store', choices=azure_devops_connection.REPOSITORIES,
                        help='Zeigt Infos für ein Azure DevOps Repository an')
    parser.add_argument('-l', '--list', required=False,
                        dest='show_repository_list', action='store_true',
                        help='Listet alle Azure DevOps Repositories auf')

    args = parser.parse_args()

    if args.open_repository:
        azure_devops_connection.open_repository(args.open_repository)
    elif args.get_repository_info:
        azure_devops_connection.get_repository_info(args.get_repository_info)
    elif args.show_repository_list:
        azure_devops_connection.print_repository_list()
    else:
        return

if __name__ == '__main__':
    main()
