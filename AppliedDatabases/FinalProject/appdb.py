# Applied Databases Final Project 2024
# Author: Norbert Antal
# 2024


from dao import DAO
import pandas as pd  

#Menu - selector
def main():
    #display_menu() # didn't work properly, functions moved to main()
    while True:
        print("")
        print("=" *36)
        print("\t\tMENU")
        print("=" *36)
        print("1 - View Cities by Country") #
        print("2 - Update City Population") #
        print("3 - Add New Person")
        print("4 - Delete Person")
        print("5 - View Countries by Population")
        print("6 - Show Twinned Cities")
        print("7 - Twin with Dublin")
        print("x - Exit Application")
        choice = input("MENU Choice: ")
        if choice == "1": # read cities
            country = input("Enter a country name or part of it:\n")
            m01_ViewCities(country)
        elif choice == "2": # increase pop
            m02()
        elif choice == "3":# add person
            m03_AddPerson()
        elif choice == "4": # delete person
            m04_DeletePerson()
        elif choice == "5": # view countries by population
            m05_countryPop()
        elif choice == "6": # view countries by population
            m06_twinned()
        elif choice == "x": # quit
            doQuit()
        else:
            display_menu()
#Menu01 - Read cities ----------------------------------------------------------------------------------        
def m01_ViewCities(country):
#The user enters a country name or part of it. User is then shown the following details of cities in that country/those countries: 
# • Country Name • City Name • City District • City Population # in groups of 2
# If the user presses any key except q the details of the next 2 cities in that country/those countries are shown. 
# Pressing q returns to the Main Menu. 
    result = DAO.CitiesByCountry_(country) # run SQL script in DAO and store result
    df=pd.DataFrame(result) #convert to dataframe
    if not df.empty:
        n=0
        while n<len(df):
            formatted_rows = df.iloc[n:n+2].apply( # display only 2 rows
                lambda x: ' | '.join( # add | between columns (https://www.reddit.com/r/learnpython/comments/nnuzoe/pandas_df_how_to_add_thousand_separators_to_a/)
                    f"{val:<15}" for val in x  # set column width 
                ),
                axis=1
            )
            print('\n'.join(formatted_rows))
            uinp=input("-- Quit (q) --") # check for q input and quit
            if uinp=="q":
                main()
                break
            else:
                n=n+2 # otherwise set .iloc to next 2 rows
    else:
        print(f"No matches found for >{country}<. Please enter a valid country name (or part thereof).") # handle invalid country name
        main()

#Menu02 - Update City population ---------------------------------------------------------------------------
def m02_UpdateCities(ID):
# The user is asked to enter a City ID: 
# When a valid City ID is entered the following details of the city are shown: 
#• ID • Name • CountryCode • Population • latitude • longitude 
# The user is then asked whether he/she wishes to Increase or Decrease the City’s Population, and by how much.

# read city by given ID
    result = DAO.ReadCity_(ID) #run SQL script and store result
    df=pd.DataFrame(result) # convert result to dataframe
    if not df.empty:
        formatted_rows = df.apply( # format output with | dividers + set column width
            lambda x: ' | '.join(
                f"{val if val is not None else 'None':<1}" for val in x # print 'None' if the value is None (otherwise unsupported format error)
            ),
            axis=1
        )
        #print("\n")
        print("\n".join(formatted_rows)) # ommit index column
    else:
        print(f"\n(!) No data found for the given City ID: {ID}.") # wrong ID handling
        m02()
# increase/decrease & set amount
    IorD = input("\n[I]ncrease/[D]ecrease Population: ")
    amount = 0
    countryID = df["ID"].iloc[0]
    
    if IorD.lower() == "i":
        act="Increased"
        try:
            amount = int(input("Enter Population Increase: "))
        except ValueError:
            print("(!) Entry must be a number. No change was made") # error handling - invalid popultaion entry
            amount=0
            m02()
    elif IorD.lower() == "d":
        act="Decreased"
        try:
            amount = -int(input("Enter Population Decrease: "))
        except ValueError:
            print("(!) Entry must be a number. No change was made") # error handling - invalid popultaion entry
            amount=0
            m02()
    elif IorD.lower() == "x": # exit option
        main()
    else:
        print("(!) Invalid input. Please enter 'I' or 'D' (or X for exit)") # I/D error handling
        m02_UpdateCities(ID)

    DAO.UpdateCity_(amount, countryID) # run SQL to update the population as per above
    print(f'\nPopulation for (ID: {df["ID"].iloc[0]}) "{df["Name"].iloc[0]}" {act} by {amount}')
    main()

def m02():# Menu2 - city ID entry + error handling
    while True:
        ID = input("\nEnter City ID: ")
        if ID.lower() == "x":
            main()
        elif not ID.isdigit():
            print("Invalid input. Please enter a number. Or 'X' to exit.")
            m02()
        else:
            m02_UpdateCities(ID)
#Menu3 - Add Person --------------------------------------------
def m03_num(txt):# Menu3 error handling - numeric entry only
        try:
            entry = int(input(f"{txt}"))
            return(entry)
        except ValueError:
            print("Entry must be a number.")
            return m03_num(txt)   
def m03_AddPerson():
    # personID, personname, age, salary, city
    print("\nAdd a person...")
    personID=m03_num("ID: ")#int(input("ID: "))
    personname=input("Name: ")
    age=int(m03_num("Age: "))
    salary=int(m03_num("Salary : "))
    city=int(m03_num("City : "))
    # run SQL & check for errors-----
    try:
        DAO.createPerson_(personID, personname, age, salary, city)
    except Exception as e:
        if "Duplicate entry" in str(e):
            print(f"\nDuplicate entry error: This person ID: {personID} already exists.\nReturning to MAIN MENU...")
            main()
        elif "foreign key constraint fails" in str(e):
            print(f"\nThe city ID: {city} does not exist.\nReturning to MAIN MENU...")
            main()
        elif "Out of range" in str(e):
            print("\nOut of range error: The city ID is out of range.\nReturning to MAIN MENU...")
            main()
        else:
            print("\nUnhandled exception:\n", e,"\nReturning to MAIN MENU...")
            main()
# Menu4 Delete Person if not visited cities
def m04_DeletePerson():
    #The user is asked to enter the ID of the person to be deleted. 
    #ERROR CONDITIONS: If the person with the specified ID has visited cities, he/she should not be deleted from the database, and the user should be returned to the main menu. 
    personID=m03_num("Enter ID of Person to Delete :")
    try:
        DAO.delPerson_(personID)
    except Exception as e:
        if "Out of range" in str(e):
            print("\n(!) Out of range error: The Person ID is out of range.\nReturning to MAIN MENU...")
            main()
        elif "foreign key constraint fails" in str(e): #ON DELETE CASCADE is not specified in either of the sql tables (person and hasvisitedcity), default is RESTRICT, resulting error below which can be used as trigger.
                                                       #Error: 1451 (23000): Cannot delete or update a parent row: a foreign key constraint fails (`appdbproj`.`hasvisitedcity`, CONSTRAINT `fk_personid` FOREIGN KEY (`personID`) REFERENCES `person` (`personID`))
            print(f"\n(!) Can't delete Person ID: {personID}. He/She has visited cities. \nReturning to MAIN MENU...")
            main()
        else:
            print("\n(!) Unhandled exception:\n", e,"\nReturning to MAIN MENU...")
            main()
# Menu 5 - View Countries by population
# The user is asked to enter <, > or =, followed by a population. For any country whose population is <, > or = (as appropriate) the population entered by the user, 
# the following information is shown: • Code • Name • Continent • Population 
# Error Conditions The user is continually prompted for one of the valid comparison operators, <, > or =, until a valid one is entered. 
def m05_countryPop________():
    while True:
        print("\nCountries by Population")
        print("-" * 10)
        result=""
        pop=0
        df=None
        usrchoice = input("\nEnter <, > or = : ")
        if usrchoice.lower() in ("<", ">", "="):
            try:
                pop = int(input("Enter Population: "))
                result = DAO.CountriesbyPop_(usrchoice, pop)
                df = pd.DataFrame(result)
            except ValueError:
                print("(!) Population entry must be a number.")
                m05_countryPop()  # Call the function again for retry
            pop = 0  # Set pop to 0 as a default after error
        elif usrchoice.lower() == "x":
            main()
        else:
            print(f"(!) Invalid input: {usrchoice}. Please enter <, > or = (or X for exit)")
            m05_countryPop()  # Call the function again for retry

        if df is not None and not df.empty:  # Check if result is not empty
            formatted_rows = df.apply(lambda x: ' | '.join(
            f"{val:<10}" for val in x  # Set column width at val:
            ), axis=1)
            print('\n'.join(formatted_rows)) # removes index column
        else:
            print(f"No matches found for ( {usrchoice}{pop} )range.")
            main()


def m05_countryPop():
    while True:
        print("\nCountries by Population")
        print("-" * 10)
        result = ""
        pop = 0
        df = None
        usrchoice = input("\nEnter <, > or = : ")
        if usrchoice.lower() in ("<", ">", "="):
            try:
                pop = int(input("Enter Population: "))
                result = DAO.CountriesbyPop_(usrchoice, pop)
                df = pd.DataFrame(result)
            except ValueError:
                print("(!) Population entry must be a number.")
                pop = 0  # Set pop to 0 after error
                continue
        elif usrchoice.lower() == "x":
            main()
        else:
            print(f"(!) Invalid input: {usrchoice}. Please enter <, > or = (or X for exit)")
            continue  # Continue to the beginning of the loop to retry

        if df is not None and not df.empty:  # Check if result is not empty
            formatted_rows = df.apply(lambda x: ' | '.join(
                f"{val:<10}" for val in x  # Set column width at val:
            ), axis=1)
            print('\n'.join(formatted_rows))  # removes index column
            main()
        else:
            print(f"No matches found for ( {usrchoice}{pop} ) range.")
            main()
            break  # Continue to the beginning of the loop to retry

def m06_twinned():
    print("\nTwinned Cities")
    print("-"*14)
    df=pd.DataFrame(DAO.neo4j_twinned_())
    if df is not None and not df.empty:  # Check if result is not empty
            formatted_rows = df.apply(lambda x: ' <->  '.join(
                f"{val:<10}" for val in x  # Set column width at val:
            ), axis=1)
            print('\n'.join(formatted_rows))  # removes index column
            main()
    #print(df.to_string(index=False, header=False))

#display menu-------
def display_menu():
    print("")
    print("=" *36)
    print("\t\tMENU")
    print("=" *36)
    print("1 - View Cities by Country") #
    print("2 - Update City Population") #
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