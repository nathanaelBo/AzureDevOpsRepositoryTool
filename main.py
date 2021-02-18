import argparse
import azure_devops_connection

def main():
    azure_devops_connection.init()

    parser = argparse.ArgumentParser(description='Open Azure DevOps Git Repo')

    parser.add_argument('-o', '--open', type=str, required=False, dest='open_repo', action='store', choices=azure_devops_connection.REPOS, help='Öffnet ein Azure DevOps Repository im Browser')
    parser.add_argument('-i', '--info', type=str, required=False,
                        dest='get_repo_info', action='store', choices=azure_devops_connection.REPOS,
                        help='Zeigt Infos für ein Azure DevOps Repository an')
    parser.add_argument('-l', '--list', required=False,
                        dest='show_repo_list', action='store_true',
                        help='Listet alle Azure DevOps Repositories auf')

    args = parser.parse_args()

    if args.open_repo:
        azure_devops_connection.open_repo(args.open_repo)
    elif args.get_repo_info:
        azure_devops_connection.get_repo_info(args.get_repo_info)
    elif args.show_repo_list:
        azure_devops_connection.print_repo_list()
    else:
        return

if __name__ == '__main__':
    main()
