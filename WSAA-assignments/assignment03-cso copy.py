# week 3 assignment 
# Assignment: data from CSO
    # Write a program that retrieves the dataset for the "exchequer account (historical series)" from the CSO, and stores it into a file called "cso.json".
# Author: Norbert Antal

# Exchequer Account (Historical Series) RESTful API data in JSON-stat format:
# https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/FIQ02/JSON-stat/2.0/en
# relevant table: FIQ02
# dimensions:     "STATISTIC",    "C02568V03113",    "TLIST(Q1)"

import requests
import json

urlBeginning="https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/"
urlEnd="/JSON-stat/2.0/en"

# first step - get response (for later to be wrintten into file)
def getAll(dataset):
    url= urlBeginning+dataset+urlEnd
    response = requests.get(url)
    return response.json()

# get response and write it straight into a json file.
def getAllAsFile(dataset):
    url= urlBeginning+dataset+urlEnd
    with open(f"all_cso{dataset}.json", "wt") as fp:
        print(json.dumps(getAll("FIQ02")), file = fp)

def getFormattedAsFile(dataset):
    with open("cso.json", "wt") as fp:
        print(json.dumps(getFormatted(dataset)), file=fp)

def getFormatted(dataset):
    data=getAll(dataset)
    ids=data["id"]
    values = data["value"]
    dimensions = data["dimension"]
    sizes = (data["size"])
    valuecount=0
    result={}
    
    #unpacking JSON with for loops
# relevant table: FIQ02
# dimensions:     "STATISTIC",    "C02568V03113",    "TLIST(Q1)"
    
    #unpack 1st dimension STATISTIC
    for dim0 in range(0, sizes[0]):
        currentId = ids[0]
        index=dimensions[currentId]["category"]["index"][dim0]
        label0=dimensions[currentId]["category"]["label"][index]
        result[label0]={}   
        #unpack 2nd dimension TLIST(A1)
        for dim1 in range(0, sizes[1]):
            currentId = ids[1]
            index=dimensions[currentId]["category"]["index"][dim1]
            label1=dimensions[currentId]["category"]["label"][index]
            #print("\t",label1)
            result[label0][label1]={} 
                #unpack 3rd dimension C02199V02655
            for dim2 in range(0, sizes[2]):
                currentId = ids[2]
                index=dimensions[currentId]["category"]["index"][dim2]
                label2=dimensions[currentId]["category"]["label"][index]
                result[label0][label1][label2]=values[valuecount]         
                valuecount+=1
    return(result)
                
                
if __name__ == "__main__":
    #getAllAsFile("FIQ02")
    getFormattedAsFile("FIQ02")
