# The following python application is based on the following databases: 
# • MySQL appdbproj. 
# • Neo4j Download appDBCity_Neo4j.txt

import mysql.connector
from dao import DAO
import pandas as pd

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="appdbproj"
)
if connection.is_connected():
    print("Connected to MySQL database")

def main():
    display_menu()
    while True:
        choice=input("Menu Choice: ")
        if (choice == "1"):
             country=input("Enter a country name or part of it:\n")
             m01_ViewCities(country)
        elif (choice == "x"):
             doQuit()
        else:
             display_menu()
             break
        
def m01_ViewCities(country):
#The user enters a country name or part of it.
# User is then shown the following details of cities in that country/those countries: 
# • Country Name • City Name • City District • City Population 
# in groups of 2
# If the user presses any key except q the details of the next 2 cities in that country/those countries are shown. 
# Pressing q returns to the Main Menu. 
    result = DAO.CitiesByCountry_(f'''select country.Name as Country, city.Name as City, 
                                             city.District as District, city.Population as Population 
                                             from city 
                                             inner join country on city.CountryCode = country.code
                                  where country.Name like "%{country}%";
                                             ''')
    df=pd.DataFrame(result)
    n=0
    while n<len(df):
        #print(df.iloc[n:n+2].to_string(index=False, header=False, justify='match-parent'))
        print(df.iloc[n:n+2].apply(lambda row: ' | '.join(map(str, row)), axis=1).to_string(index=False, header=False))

        uinp=input("-- Quit (q) --")
        if uinp=="q":
             main()
             break
        else:
             n=n+2

def display_menu():
    print("")
    print("=" *50)
    print("\t\t\tMENU")
    print("=" *50)
    print("1 - View Cities by Country")
    print("2 - Update City Population")
    print("3 - Add New Person")
    print("4 - Delete Person")
    print("5 - View Countries by Population")
    print("6 - Show Twinned Cities")
    print("7 - Twin with Dublin")
    print("x - Exit Application")

def doQuit():
    print("Thank you!")
    exit()

if __name__ == "__main__":
	# execute only if run as a script 
	main()