# Data Access Object (DAO) for Applied Databases Final Project 2024 
# Data sources: • MySQL appdbproj. # • Neo4j Download appDBCity_Neo4j.txt

# ------------- test presence / install mySQL-connector module ------------------ #https://stackoverflow.com/questions/6120902/how-do-i-automatically-install-missing-python-modules
import traceback
import os
import neo4j

try: 
    import mysql.connector
    if not hasattr(mysql.connector, 'connect'):
        raise AttributeError("Attribute 'connect' not found in mysql.connector")
except ImportError:
    print("Required module missing: mysql.connector\n")
    traceback.print_exc()
except AttributeError as e:
    print("""
    .
    .
    Required module missing: mysql.connector\n""")
    print("""...Installing missing module now... 
    
    Please restart the program after installation finished
    
    """)
    os.system('python -m pip install mysql-connector-python')
    exit()
#------------------------------------------------------------------------------
try: 
    import neo4j
    if not hasattr(mysql.connector, 'connect'):
        raise AttributeError("Attribute 'connect' not found in neo4j")
except ImportError:
    print("Required module missing: neo4j\n")
    traceback.print_exc()
except AttributeError as e:
    print("""
    .
    .
    Required module missing: neo4j\n""")
    print("""...Installing missing module now... 
    
    Please restart the program after installation finished
    
    """)
    os.system('python -m pip install neo4j')
    exit()
#------------------------------------------------------------------------------

import mysql.connector
from config import config_mysql as cfg
from neo4j import GraphDatabase

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
        cursor.execute('''select country.Name as Country, city.Name as City,
                                             city.District as District, city.Population as Population 
                                             from city 
                                             inner join country on city.CountryCode = country.code
                                  where country.Name like %s''',(f'%{country}%',))
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
        cursor.execute('''SELECT ID, Name, CountryCode, Population, latitude, longitude
                      FROM city
                      WHERE ID = %s''', (ID,))
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
        amount =int(amount)
        countryID=int(countryID)
        cursor = self.getCursor()
        cursor.execute('''UPDATE city SET Population = Population + %s WHERE ID = %s''', (amount, countryID))
        self.connection.commit()
        self.closeAll()    

# Menu 3 - Add Person
    def createPerson_(self, personID, personname, age, salary, city):
        try:
            cursor = self.getCursor()
            cursor.execute('''INSERT INTO person (personID, personname, age, salary, city)
                          VALUES (%s, %s, %s, %s, %s)''', (personID, personname, age, salary, city))
            self.connection.commit()
        except Exception as e:
            #print("Error:", e)  # Print the error message
            raise e  # Re-raise the exception
        finally:
            print("Person Added: ID:", personID,"| Name:",personname,"| Age: ",age,"| Salary:",salary,"| CityID:",city)
            self.closeAll()

# Menu 4 - Delete person if not visited city
    def delPerson_(self,personID):
        try:
            cursor = self.getCursor()
            cursor.execute("DELETE FROM person WHERE personID = %s", (personID,))
            if cursor.rowcount == 0:
                print(f"\n (!) Person ID {personID} not found. Nothing deleted.")
            else:
                self.connection.commit()
                print(f"\nPerson ID {personID} deleted.")
        except Exception as e:
            print("Error:", e)  # Print the error message
            raise e  # Re-raise the exception
        finally:
            self.closeAll()
# Menu 5 - Countries by population
    def CountriesbyPop_(self, usrchoice, pop):
        pop=int(pop)
        cursor = self.getCursor()
        cursor.execute(f'''select Code, Name, Continent, Population from country 
                            where Population {usrchoice}{pop};''')#,(usrchoice, pop))
        result = cursor.fetchall()
        resultlist = []
        for row in result:
            resultlist.append(self.convDict_ReadCountbyPop(row))
        self.closeAll()
        return resultlist
    
    def convDict_ReadCountbyPop(self,resultLine):
        CountKeys = [
        "Code", "Name", "Continent", "Population"]
        currentkey = 0
        result = {}
        for attrib in resultLine:
            result[CountKeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return result
    
# Menu 6 Neo4j - 
    def neo4j_twinned_(self):
        
        # Connect to the Neo4j database
        uri = "neo4j+s://fdf8e32f.databases.neo4j.io"
        driver = GraphDatabase.driver(uri, auth=("neo4j", "0K9KDPJ-dY3E3QAZ1HhGNX0rSIH1VPxPPxXIEl2Sj7o"))

        # Run a query
        with driver.session() as session:
            result = session.run("match(c)-[]-(c2) return c.name, c2.name order by c.name")
            
                # Fetch all results into a list of dictionaries
            records = [dict(record) for record in result]
        
        '''for record in records:
            print(record)'''

            # Close the driver
        driver.close()
        return(records)

DAO = DAO()