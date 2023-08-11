import json
import requests
from argparse import ArgumentParser

def check_appname(restURL, api_key, application):
    url=f"{restURL}/api/applications"
    headers = {
        "x-api-key": api_key
    }

    try:
        #fetching the Application list and details.
        rsp = requests.get(url, headers=headers)
        # print(rsp.status_code)
        if rsp.status_code == 200:
            apps = json.loads(rsp.text) 
            app_dict = {}
            for app in apps['applications']:
                app_dict[app["name"]] = app["guid"]

            if application not in app_dict.keys():
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
    parser.add_argument('-restURL','--restURL',required=True,help='CAST Console REST API URL')
    parser.add_argument('-api_key','--api_key',required=True,help='CAST Console API KEY')
    parser.add_argument('-application','--application',required=True,help='Application Name')

    args=parser.parse_args()
    result = check_appname(args.restURL, args.api_key, args.application)
    print(result)
