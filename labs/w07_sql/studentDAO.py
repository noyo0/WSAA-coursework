import mysql.connector

class StudentDAO:
    host = ""
    user = ""
    password = ""
    database = ""
    connection = ""
    cursor = ""

    def __init__(self):
        # These values should ideally be read from a config file
        self.host = "localhost"
        self.user = "root"
        self.password = "root"
        self.database = "wsaa"

    def getCursor(self):
        # Establish a connection and return a cursor object
        self.connection = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )
        self.cursor = self.connection.cursor()
        return self.cursor

    def closeAll(self):
        # Close the connection and cursor
        self.connection.close()
        self.cursor.close()

    def create(self, values):
        # Create a new record in the database
        cursor = self.getCursor()
        sql = "INSERT INTO student (name, age) VALUES (%s, %s)"
        cursor.execute(sql, values)
        self.connection.commit()
        new_id = cursor.lastrowid
        self.closeAll()
        return new_id

    def getAll(self):
        # Retrieve all records from the database
        cursor = self.getCursor()
        sql = "SELECT * FROM student"
        cursor.execute(sql)
        result = cursor.fetchall()
        studentlist =[]
        for row in result:
            studentlist.append(self.convertToDict(row))
        self.closeAll()
        return result

    def findByID(self, id):
        # Retrieve a record by its ID
        cursor = self.getCursor()
        sql = "SELECT * FROM student WHERE id = %s"
        cursor.execute(sql, (id,))
        result = cursor.fetchone()
        self.closeAll()
        return result.convertToDict(result)

    def update(self, values):
        # Update a record in the database
        cursor = self.getCursor()
        sql = "UPDATE student SET name = %s, age = %s WHERE id = %s"
        cursor.execute(sql, values)
        self.connection.commit()
        self.closeAll()

    def delete(self, id):
        # Delete a record from the database
        cursor = self.getCursor()
        sql = "DELETE FROM student WHERE id = %s"
        cursor.execute(sql, (id,))
        self.connection.commit()
        self.closeAll()

    def convertToDict(self,resultLine):
        studentKeys = ["id","name","age"]
        currentkey=0
        student={}
        for attribute in resultLine:
            student[studentKeys[currentkey]] = attribute
        return student
        
# Create an instance of StudentDAO
studentDAO = StudentDAO()
