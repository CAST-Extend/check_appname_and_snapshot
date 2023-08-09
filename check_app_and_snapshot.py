import json
from requests.auth import HTTPBasicAuth
import requests
from argparse import ArgumentParser

def check_appname():
    method = "get"
    url=f"{args.restURL}/api/applications"
    auth = HTTPBasicAuth(f'{args.user}', f'{args.password}')

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
                return 1
            else:
                return 0

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

    args=parser.parse_args()
    # aip = AipRestCall(args.restURL, args.user, args.password)
    result = check_appname()
    print(result)
