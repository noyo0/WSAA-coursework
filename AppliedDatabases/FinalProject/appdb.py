# Final Project
# SQL interactions are through dao.py DAO


from dao import DAO
import pandas as pd

def m02():
    while True:
        ID = input("\nEnter City ID:\n")
        if ID.lower() == "x":
            main()
        elif not ID.isdigit():
            print("Invalid input. Please enter a number. Or 'X' to exit.")
            m02()
        else:
            m02_UpdateCities(ID)
    

#Menu
def main():
    display_menu()
    while True:
        choice = input("MENU Choice: ")
        if choice == "1":
            country = input("Enter a country name or part of it:\n")
            m01_ViewCities(country)
        elif choice == "2":
            m02()
        elif choice == "x":
            doQuit()
        else:
            display_menu()
        
def m01_ViewCities(country):
#The user enters a country name or part of it. User is then shown the following details of cities in that country/those countries: 
# • Country Name • City Name • City District • City Population # in groups of 2
# If the user presses any key except q the details of the next 2 cities in that country/those countries are shown. 
# Pressing q returns to the Main Menu. 
    result = DAO.CitiesByCountry_(f'''select country.Name as Country, city.Name as City,
                                             city.District as District, city.Population as Population 
                                             from city 
                                             inner join country on city.CountryCode = country.code
                                  where country.Name like "%{country}%";
                                             ''')
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


def m02_UpdateCities(ID):
# The user is asked to enter a City ID: 
# When a valid City ID is entered the following details of the city are shown: 
#• ID • Name • CountryCode • Population • latitude • longitude 
# The user is then asked whether he/she wishes to Increase or Decrease the City’s Population, and by how much.
    result = DAO.ReadCity_(f'''select ID, Name, CountryCode, Population, latitude, longitude
                                  from city
                                  where ID={ID};''')
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
    
    IorD = input("\n[I]ncrease/[D]ecrease Population: ")
    amount = 0
    cID = df["ID"].iloc[0]
    
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
    # Update the population via SQL
    sql_script = f'''UPDATE city SET Population = Population + {amount} WHERE ID = {cID};'''
    DAO.UpdateCity_(sql_script)
    print(f'\nPopulation for (ID: {df["ID"].iloc[0]}) "{df["Name"].iloc[0]}" {act} by {amount}')
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