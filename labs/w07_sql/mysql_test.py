# Test MySQL via python

import mysql.connector  

# Establish connection to MySQL server
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root"
)
# Create a cursor object to execute SQL queries
mycursor = connection.cursor()

### Print the names of existing databases ###
def printall(): 
# Execute a query to select existing databases
    mycursor.execute("SHOW DATABASES")
# Fetch all rows (databases) from the result set
    databases = mycursor.fetchall()
#Print results
    print("LIST OF DATABASES:")
    for database in databases:
        print(database[0])

### create new database ### 
def createnewdb(name):
# Create a cursor object to execute SQL queries
# Execute a SQL query to create a new database named 'wsaa'
    mycursor.execute(f"CREATE DATABASE {name}")


# create table in existing database
# create table in database
def createtable():
    #connect to the specific database
    mydb = mysql.connector.connect(
    host="localhost",     # MySQL server hostname
    user="root",          # MySQL username
    password="root",          # MySQL password
    database="wsaa"       # Name of the database to use
)
    mycursor = mydb.cursor() #this is a new cursor, could work in tandem with the other one
# SQL statement to create a table named 'student'
    sql = "CREATE TABLE student (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), age INT)"
# Execute the SQL statement to create the table
    mycursor.execute(sql)

def createStudent(values):
    #connect to the specific database
    mydb = mysql.connector.connect(
    host="localhost",     # MySQL server hostname
    user="root",          # MySQL username
    password="root",          # MySQL password
    database="wsaa"       # Name of the database to use
)
    mycursor = mydb.cursor() #this is a new cursor, could work in tandem with the other one
# SQL statement to create a table named 'student'
    sql = "INSERT INTO student (`name`, `age`) VALUES (%s, %s)"
# Execute the SQL statement to create the table
    mycursor.execute(sql)
    mydb.commit()

def runSQLinwsaa(sql):
    #connect to the specific database
    mydb = mysql.connector.connect(
    host="localhost",     # MySQL server hostname
    user="root",          # MySQL username
    password="root",          # MySQL password
    database="wsaa"       # Name of the database to use
)
    mycursor = mydb.cursor() #this is a new cursor, could work in tandem with the other one
# Execute the SQL statement to create the table
    mycursor.execute(sql)
# print output
    output=mycursor.fetchall()
    print("MySQL output:")
    for o in output:
        print(o)

def getOutput(sql): 
        #connect to the specific database
    mydb2 = mysql.connector.connect(
    host="localhost",     # MySQL server hostname
    user="root",          # MySQL username
    password="root",          # MySQL password
    database="wsaa"       # Name of the database to use
)
    mycursor = mydb2.cursor() #this is a new cursor, could work in tandem with the other one
# Execute a query to select existing databases
    mycursor.execute(sql)
# Fetch all rows (databases) from the result set
    databases = mycursor.fetchall()
#Print results
    print("output:")
    for database in databases:
        print(database)

#test------------------------
#printall()
#runSQLinwsaa("INSERT INTO student (`name`, `age`) VALUES ('bob', 25)")
createStudent(("Darth",54))
getOutput("select * from student")
#createnewdb('wsaa')
#printall()

#-----------CLOSE EVERYTHING--------------------------
# Close the cursor (release database resources)
mycursor.close()
# close connection when all finished
connection.close()