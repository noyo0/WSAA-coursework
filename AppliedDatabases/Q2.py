
# Main function
array=[]
def main():
	# Initialise array
	#display_menu()
	global array
	while True:
		display_menu()
		choice = input("Enter menu choice: ")
		
		if (choice == "1"):
			array = fill_array()
		elif (choice == "2"):
			print(f"\nCurrently stored:\n{array}")
			#display_menu()
		elif (choice == "3"):
			find_gt_in_array(array)
			#display_menu()
		elif (choice == "4"):
			doQuit()
		else:
			display_menu()

def fill_array():
	# fill array with numbers or exit with x
    global array
    print("Add numbers to array (enter -1 for quick list or x to exit to main menu)")
    while True:
        user_input=input("Add number (or x to exit):")
        if user_input == '-1':
            print("currently stored:\n")
            print(f"{array}\n")            		
        elif user_input == 'x':
            main()
            break
        elif user_input == None:
            main()
            break
        elif not user_input.isdigit():
            user_input=print("Invalid input. Exit to Menu.")
            main()
        else:
            array.append(user_input)


def find_gt_in_array(array):
# Write the necessary code to get a number from the user
# and print out all numbers in the array that are greater
# than this number
	greater=int(input("print numbers greater than: "))
	int_array = [int(element) for element in array]
	greater_array=[]
	for a in int_array:
		if a>greater:
			greater_array.append(a)
			
	print(f"\nnumber greater than {greater}: \n{greater_array}")

    
def display_menu():
    print("")
    print("MENU")
    print("=" * 4)
    print("1 - Fill Array")
    print("2 - Print Array")
    print("3 - Find > in Array")
    print("4 - Exit")

def doQuit():
    print("Thank you!")
    exit()
	
if __name__ == "__main__":
	# execute only if run as a script 
	main()
