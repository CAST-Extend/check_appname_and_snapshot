import json
from requests.auth import HTTPBasicAuth
import requests
from cast_common.util import run_process
from argparse import ArgumentParser

def create_app(args):
    print('Creating new application.....\n')
    args = ['java', '-jar', args.console_cli, 'new', '-n', args.application, '--apikey', args.console_key, '--verbose=false', '--no-version-history=false', f'-css="Server-Host:{args.css_port}"' ]
    try:
        process = run_process(args,wait=True)
    except FileNotFoundError as e:
        print(f'Unable to create application {args.application} -> {e}')
        return e.errno
    
def add_new_version_and_take_snapshot(args):
    print('Adding new version and taking snapshot.....\n')
    args = ['java', '-jar', args.console_cli, 'add', f'--apikey={args.console_key}', '-n', args.application, '-f', args.source_code_loc, '--verbose=false']
    try:
        process = run_process(args,wait=True)
    except FileNotFoundError as e:
        print(f'Unable to add a new version and analyze its source code application {args.application} -> {e}')
        return e.errno

def check_snapshot(args, guid):
    method = "get"
    url=f"{args.restURL}/rest/{guid}/applications/3/snapshots"
    auth = HTTPBasicAuth('apikey', f'{args.console_key}')

    try:
        #fetching the Application list and details.
        rsp = requests.request(method, url, auth=auth)
        # print(rsp.status_code)
        if rsp.status_code == 200:
            apps = json.loads(rsp.text) 

            if len(apps)  <= 0:
                print(f'No snapshots found for the Application -> {args.application}.\n')
                add_new_version_and_take_snapshot(args)
                exit(-1)
            else:
                print(f"snapshots found for the Application -> {args.application}.\n")

        else:
            print("Some error has occured! ")
            print(rsp.text)

    except Exception as e:
        print('some exception has occured! \n Please resolve them or contact developers')
        print(e)


if __name__ == "__main__":

    parser = ArgumentParser()
    parser.add_argument('-restURL','--restURL',required=True,help='CAST REST API URL')
    parser.add_argument('-user','--user',required=True,help='CAST REST API User Name')
    parser.add_argument('-password','--password',required=True,help='CAST REST API Password')
    parser.add_argument('-application','--application',required=True,help='Application Name')

    parser.add_argument('-console_cli','--console_cli',required=True,help='Console CLI')
    parser.add_argument('-console_key','--console_key',required=True,help='Console Key')
    parser.add_argument('-css_port','--css_port',required=True,help='CSS Port')
    parser.add_argument('-source_code_loc','--source_code_loc',required=True,help='Source Code Location')

    args=parser.parse_args()
    # aip = AipRestCall(args.restURL, args.user, args.password)

    method = "get"
    url=f"{args.restURL}/api/applications"
    auth = HTTPBasicAuth('apikey', f'{args.console_key}')

    try:
        #fetching the Application list and details.
        rsp = requests.request(method, url, auth=auth)
        # print(rsp.status_code)
        if rsp.status_code == 200:
            apps = json.loads(rsp.text) 
            app_dict = {}
            for app in apps['applications']:
                app_dict[app["name"]] = app["guid"]

            if args.application not in app_dict.keys():
                print(f"{args.application} is not present in the AIP console.\n")
                create_app(args)
                add_new_version_and_take_snapshot(args)
            else:
                print(f"{args.application} is already present in the AIP console.\n")
                check_snapshot(args, app_dict[args.application])

        else:
            print("Some error has occured! ")
            print(rsp.text)

    except Exception as e:
        print('some exception has occured! \n Please resolve them or contact developers')
        print(e)


