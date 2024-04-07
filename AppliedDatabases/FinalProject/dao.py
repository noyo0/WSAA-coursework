# Data Access Object (DAO) for # • MySQL appdbproj. # • Neo4j Download appDBCity_Neo4j.txt

import mysql.connector
from config import config_mysql as cfg

class DAO:
    host =""
    user = ""
    password =""
    database =""

    connection = ""
    cursor =""
#authentication & initialisation
    def __init__(self): 
        self.host=cfg["host"]
        self.user=cfg["user"]
        self.password=cfg["password"]
        self.database="appdbproj"
    
    def getCursor(self): 
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self.cursor
    
    def closeAll(self):
        self.connection.close()
        self.cursor.close()
    
# commands
    def CitiesByCountry_(self, sql_query):
        cursor = self.getCursor()
        cursor.execute(sql_query)
        result = cursor.fetchall()
        resultlist = []
        for row in result:
            resultlist.append(self.convDict_city(row))
        self.closeAll()
        return resultlist


    def convDict_city(self,resultLine):
        CityKeys = [
        "Country", "City", "District", "Population"
    ]
        currentkey = 0
        result = {}
        for attrib in resultLine:
            result[CityKeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return result
    

DAO = DAO()
