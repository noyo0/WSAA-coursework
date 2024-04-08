# Final Project
# SQL interactions are through dao.py DAO


from dao import DAO
import pandas as pd  

#Menu - selector
def main():
    #display_menu()
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
        elif choice == "x":
            doQuit()
        else:
            display_menu()
#Menu01 - Read cities ----------------------------------------------------------------------------------        
def m01_ViewCities(country):
#The user enters a country name or part of it. User is then shown the following details of cities in that country/those countries: 
# • Country Name • City Name • City District • City Population # in groups of 2
# If the user presses any key except q the details of the next 2 cities in that country/those countries are shown. 
# Pressing q returns to the Main Menu. 
    result = DAO.CitiesByCountry_(country)
    df=pd.DataFrame(result)
    if not df.empty:
        n=0
        while n<len(df):
            #print(df.iloc[n:n+2].to_string(index=False, header=False) # simple output
            # FORMATTING - - print output formatted with | dividers and fixed width
            formatted_rows = df.iloc[n:n+2].apply(
                lambda row: ' | '.join(
                    f"{val:<15}" for val in row  # set column width at val:
                ),
                axis=1
            )
            print('\n'.join(formatted_rows))
            uinp=input("-- Quit (q) --")
            if uinp=="q":
                main()
                break
            else:
                n=n+2
    else:
        print("No data found for the given ID.")
        main()
#Menu02 - Update City population ---------------------------------------------------------------------------
def m02():# Menu2 error handling
    while True:
        ID = input("\nEnter City ID:\n")
        if ID.lower() == "x":
            main()
        elif not ID.isdigit():
            print("Invalid input. Please enter a number. Or 'X' to exit.")
            m02()
        else:
            m02_UpdateCities(ID)
def m02_UpdateCities(ID):
# The user is asked to enter a City ID: 
# When a valid City ID is entered the following details of the city are shown: 
#• ID • Name • CountryCode • Population • latitude • longitude 
# The user is then asked whether he/she wishes to Increase or Decrease the City’s Population, and by how much.

# read city by given ID
    result = DAO.ReadCity_(ID)
    df=pd.DataFrame(result)
    if not df.empty:
        formatted_rows = df.apply(
            lambda row: ' | '.join(
                f"{val if val is not None else 'None':<15}" for val in row
            ),
            axis=1
        )
        print("\n")
        print("".join(formatted_rows))
    else:
        print("No data found for the given ID.")
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
            print("Entry must be a number. No change was made")
            amount=0
            m02()
    elif IorD.lower() == "d":
        act="Decreased"
        try:
            amount = -int(input("Enter Population Decrease: "))
        except ValueError:
            print("Entry must be a number. No change was made")
            amount=0
            m02()
    elif IorD.lower() == "x":
        main()
    else:
        print("Invalid input. Please enter 'I' or 'D' (or X for exit)")
        m02_UpdateCities(ID)

# Update the population as per above
    DAO.UpdateCity_(amount, countryID)
    print(f'\nPopulation for (ID: {df["ID"].iloc[0]}) "{df["Name"].iloc[0]}" {act} by {amount}')
    main()
#Menu3 - Add Person --------------------------------------------
def m03_num(txt):# Menu3 error handling
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

def m04_DeletePerson():
    personID=m03_num("Enter ID of Person to Delete :")
    try:
        DAO.delPerson_(personID)
    except Exception as e:
        if "Out of range" in str(e):
            print("\nOut of range error: The Person ID is out of range.\nReturning to MAIN MENU...")
            main()
        else:
            print("\nUnhandled exception:\n", e,"\nReturning to MAIN MENU...")
            main()


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