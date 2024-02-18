# This is a module that provides a set of functions to interact with
# the demonstration book API hosted at PythonAnyhwere
# Author Andrew Beatty

import requests
import json
url = "http://andrewbeatty1.pythonanywhere.com/books"

def getAllBooks():
    response = requests.get(url)
    return response.json()

def getBookById(id):
    geturl = url +"/"+str(id)
    response = requests.get(geturl)
    return response.json()

def createBook(author, title, price):
    book = {
        'Author':f"{author}",
        'Title':f"{title}",
        'Price':price
    }
    #print(book)
    response = requests.post(url, json=book)

def updateBook(id, bookdiff):
        updateurl = url +"/"+str(id)
        response = requests.put(updateurl, json=bookdiff)
        return response


def deleteBook(id):
    deleteturl = url +"/"+str(id)
    response = requests.delete(deleteturl)
    return response.json()