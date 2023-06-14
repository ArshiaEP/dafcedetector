import requests
import hashlib

def sendRequest(url):
        resUrl = requests.get(url)
        resultUrl = str(resUrl.content)
        return resultUrl

def convertRequestToHash(content):
        hashUrl = hashlib.md5(content.encode())
        resApp = hashUrl.hexdigest()
        return resApp
def main():

    def get_difference(list_a, list_b):
        return set(list_a)-set(list_b)
    reqUrl = ""
    hashUrl = ""
    hashResult = convertRequestToHash(sendRequest(reqUrl))
    print("*****************************************")
    print(f"Http response code = {requests.get(reqUrl).status_code}")
    print("*****************************************")
    print(f"result hash = {hashResult}")
    print(hashResult)
    print("") if hashUrl == hashResult else print("")

if __name__ == '__main__':
        main()
