#break up API address to changeable parameters
#encapsulate below ion a separate file valoffdao.py

import requests
import json
import urllib.parse
url = "https://api.valoff.ie/api/Property/GetProperties"

# set parameters
ParametersDict={
    "Download":"false",
    "Format":"json",
    "CategorySelected":"OFFICE",
    "LocalAuthority":"WICKLOW COUNTY COUNCIL",
    "Fields":"LocalAuthority,Category,Level,AreaPerFloor,NavTotal,CarPark,PropertyNumber,IG,Use,FloorUse,Address,PublicationDate"
}

# getAll() function makes an HTTP GET request and returns the JSON response obtained from the API.
def getAll():
    parameters=urllib.parse.urlencode(ParametersDict)
    fullURTL= url+"?"+parameters
    response = requests.get(fullURTL)
    return response.json()

if __name__ == "__main__": # The if __name__ == "__main__": block ensures that the following code runs only when the script is executed directly (not when it’s imported as a module).
# write out response to json
    with open("valoff.json","wt") as fp:
        print(json.dumps(getAll()), file=fp)