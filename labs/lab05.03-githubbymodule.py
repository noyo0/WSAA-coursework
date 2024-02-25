from github import Github
from config import config as cfg
import requests

apikey = cfg

g = Github(apikey)
# list all available repositories:
for repo in g.get_user().get_repos():
    print(repo.name) 
    pass

#get repo URL
repo = g.get_repo("noyo0/WebserviceTest") 
print("API return: ",repo.clone_url)

# Get the repository contents
file_contents = repo.get_contents("")
for file_info in file_contents:
    print("Found file:", file_info.path)


# get download link of one particular file on the repo
fileInfo = repo.get_contents("test.txt") 
urlOfFile = fileInfo.download_url
#print(urlOfFile)

# get contents of a text file:
response = requests.get(urlOfFile)
file_content = response.content.decode("utf-8")
#print("File contents:\n",file_content)

# get contents another way
response = requests.get(urlOfFile) 
contentOfFile = response.text 
#print ("CONTENTS\n",contentOfFile)

#append the text in the file
newContents = contentOfFile + "\n !!!!more stuff!!!! \n" 
gitHubResponse=repo.update_file(fileInfo.path,"updated by prog", newContents,fileInfo.sha) 
print (gitHubResponse) 

# get contents another way
response = requests.get(urlOfFile) 
contentOfFile = response.text 
print ("CONTENTS\n",contentOfFile)