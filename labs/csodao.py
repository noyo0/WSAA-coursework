# getting data from CSO.ie with 4 dimensions - population stats
# https://ws.cso.ie/public/api.restful/PxStat.Data.Cube_API.ReadDataset/FP001/JSON-stat/2.0/en

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
    with open("cso.json", "wt") as fp:
        print(json.dumps(getAll("FP001")), file = fp)

def getFormattedAsFile(dataset):
    with open("cso-formatted.json", "wt") as fp:
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

    #unpack 1st dimension STATISTIC
    for dim0 in range(0, sizes[0]):
        currentId = ids[0]
        index=dimensions[currentId]["category"]["index"][dim0]
        label0=dimensions[currentId]["category"]["label"][index]
        result[label0]={}   
        #print(label0)
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
                #print("\t\t",label)
                result[label0][label1][label2]={} 
                #unpack 4th dimension C02199V02655
                for dim3 in range(0, sizes[3]):
                    currentId = ids[3]
                    index=dimensions[currentId]["category"]["index"][dim3]
                    label3=dimensions[currentId]["category"]["label"][index]
                #    print("\t\t\t",label," ", values[valuecount])
                    result[label0][label1][label2][label3]=values[valuecount]               
                    valuecount+=1
    #print(result)
    return(result)
                
                
if __name__ == "__main__":
    #getAllAsFile("FP001")
    getFormattedAsFile("FP001")