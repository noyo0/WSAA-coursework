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
# Menu 1 - CitiesByCountry
    def CitiesByCountry_(self, country):
        cursor = self.getCursor()
        cursor.execute(f'''select country.Name as Country, city.Name as City,
                                             city.District as District, city.Population as Population 
                                             from city 
                                             inner join country on city.CountryCode = country.code
                                  where country.Name like "%{country}%";
                                             ''')
        #cursor.execute(sql_query)
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
    
# Menu 2 - UpdateCity
    #read from SQL
    def ReadCity_(self, ID):
        cursor = self.getCursor()
        cursor.execute(f'''select ID, Name, CountryCode, Population, latitude, longitude
                                  from city
                                  where ID={ID};''')
        result = cursor.fetchall()
        resultlist = []
        for row in result:
            resultlist.append(self.convDict_Readcity(row))
        self.closeAll()
        return resultlist
    # format output
    def convDict_Readcity(self,resultLine):
        CityKeys = [
        "ID", "Name", "CountryCode", "Population", "latitude", "longitude"
    ]
        currentkey = 0
        result = {}
        for attrib in resultLine:
            result[CityKeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return result
    # update
    def UpdateCity_(self, amount, countryID):
        cursor = self.getCursor()
        cursor.execute(f'''UPDATE city SET Population = Population + {amount} WHERE ID = {countryID};''')
        self.connection.commit()
        self.closeAll()    

# Menu 3 - Add Person
    def createPerson_(self, personID, personname, age, salary, city):
        try:
            cursor = self.getCursor()
            cursor.execute(f'''INSERT INTO person (personID, personname, age, salary, city)
                            VALUES {personID, personname, age, salary, city};''')
            self.connection.commit()
        except Exception as e:
            #print("Error:", e)  # Print the error message
            raise e  # Re-raise the exception
        finally:
            print("Person Added: ID:", personID,"| Name:",personname,"| Age: ",age,"| Salary:",salary,"| CityID:",city)
            self.closeAll()


    def delPerson_(self,personID):
        try:
            cursor = self.getCursor()
            cursor.execute(f"DELETE FROM person WHERE personID = {personID}")
            self.connection.commit()
        except Exception as e:
            #print("Error:", e)  # Print the error message
            raise e  # Re-raise the exception
        finally:
            print(f"Person ID {personID} Deleted:")
            self.closeAll()

DAO = DAO()
