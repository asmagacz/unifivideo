import requests
import json
import argparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CamerasData:
    def __init__(self, apiUrl, apiKey):
        self.code = ''
        try:
            self.testurl = apiUrl + '?apiKey=' + apiKey
            self.cameras = []
            self.session = requests.session()
            self.requesttest = self.session.request("GET", self.testurl, verify=False).json()
            self.cameras.append(self.requesttest['data'])
        except:
            self.code = '1'
            self.checkConnection()
            exit()

    def discoverCameras(self):
        discovery = []
        for val in self.cameras:
            for key in val:
                discovery.append({"{#NAME}": key['name']})
        output = json.dumps({'data': discovery}, indent=4, ensure_ascii=False)
        return output

    def ifCameraOn(self, cameraname):
        for val in self.cameras:
            for key in val:
                if cameraname == key['name']:
                    print(key['state'])

    def showcameraip(self, cameraname):
        for val in self.cameras:
            for key in val:
                if cameraname == key['name']:
                    print(key['controllerHostAddress'])

    def showcameramac(self, cameraname):
        for val in self.cameras:
            for key in val:
                if cameraname == key['name']:
                    print(key['mac'])

    def showcameramodel(self, cameraname):
        for val in self.cameras:
            for key in val:
                if cameraname == key['name']:
                    print(key['model'])

    def lastRecordingTime(self, cameraname):
        for val in self.cameras:
            for key in val:
                if cameraname == key['name']:
                    print(int(str(key['lastRecordingStartTime'])[:-3]))

    def checkConnection(self):
        if self.code == '1':
            print('1')
        else:
            print('0')


class switch(object):
    value = None

    def __new__(class_, value):
        class_.value = value
        return True


def case(*args):
    return any((arg == switch.value for arg in args))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--method', help='method name to call')
    parser.add_argument('-p', '--parameter', help='parameter')
    parser.add_argument('-api', '--apikey', help='api key')
    parser.add_argument('-u', '--url', help='url')
    args = parser.parse_args()

    method = str(args.method).strip()
    parameter = str(args.parameter).strip()
    apikey = str(args.apikey).strip()
    url = str(args.url).strip()
    cameradata = CamerasData(url, apikey)

    # switch case
    while switch(method):
        if case('discovercameras'):
            print(cameradata.discoverCameras())
            break
        if case('ifcameraon'):
            cameradata.ifCameraOn(parameter)
            break
        if case('lastrecordingtime'):
            cameradata.lastRecordingTime(parameter)
            break
        if case('showmac'):
            cameradata.showcameramac(parameter)
            break
        if case('showip'):
            cameradata.showcameraip(parameter)
            break
        if case('showmodel'):
            cameradata.showcameramodel(parameter)
            break
        if case('checkconnection'):
            cameradata.checkConnection()
            break
        print('To run script use command: '
              'python <scriptname.py> --method<method to call> --parameter<method argument> '
              '--url<controller url> --apikey<apikey>'
              '\nAvailable parameters: '
              '\n-m, --method, help= method name to call'
              '\n-p, --parameter, help= parameter'
              '\n-u, --url, help= controller url'
              '\n-api, --apikey, help- api key'
              '\nTo call method use:'
              '\n\tpython unifivideo.py -m discovercameras -u <controller url> -api <controller api key>'
              '\n\tpython unifivideo.py -m ifcameraon -p <camera name> -u <controller url> -api <controller api key>'
              '\n\tpython unifivideo.py -m showip -p <camera name> -u <controller url> -api <controller api key>'
              '\n\tpython unifivideo.py -m showmodel -p <camera name> -u <controller url> -api <controller api key>'
              '\n\tpython unifivideo.py -m showmac -p <camera name> -u <controller url> -api <controller api key>'
              '\n\tpython unifivideo.py -m lastrecordingtime -p <camera name> -u <controller url> '
              '-api <controller api key>'
              '\n\tpython unifivideo.py -m checkconnection -u <controller url> -api <controller>')
        break

