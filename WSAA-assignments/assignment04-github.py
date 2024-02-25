# Assignment 04
#   Write a program in python that will read a file from a repository, 
#   The program should then replace all the instances of the text "Andrew" with your name. 
#   The program should then commit those changes and push the file back to the repository 
# Author: Norbert Antal

from github import Github # module to interact with Github API
from config import config # credentials
import requests # HTTP client library

apikey = config # store authentication key

g = Github(apikey) #request API access

#get repo URL
repo = g.get_repo("noyo0/WebserviceTest") 
#print("API return: ",repo.clone_url)

'''# Get the repository contents
file_contents = repo.get_contents("")
for file_info in file_contents:
    print("repo content:", file_info.path)'''

# get direct URL of target file on the repo
fileInfo = repo.get_contents("Andrew.txt") 
urlOfFile = fileInfo.download_url
#print(urlOfFile)

# get contents of file above
response = requests.get(urlOfFile) 
contentOfFile = response.text 

#append the text in the file
#newContents = contentOfFile.replace("Kubla Khan","Andrew") # https://www.w3schools.com/python/ref_string_replace.asp
newContents = contentOfFile.replace("Andrew","Norbert")
gitHubResponse=repo.update_file(fileInfo.path,"updated by assignment04-github.py", newContents,fileInfo.sha) 
print (gitHubResponse) 

#check file content after change
response = requests.get(urlOfFile) 
contentOfFile = response.text 
print ("CONTENTS\n",contentOfFile)