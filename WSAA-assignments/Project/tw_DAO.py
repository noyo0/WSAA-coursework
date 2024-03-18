# Data Access Object (DAO) for truckwash
# datatable: tw_transactions
# sample:
#+-----------+----------------+-------------+-------------+---------+-------+-----------+------+-------+-----------+------------+---------+------------+----+------------------+
#| MoveIT ID | FleetNumber    | Third party | source_Date | EQ Type | Rate  | JV        | Year | Month | Dayname   | Reg        | TP Code | Weeknumber | id | Transaction_Date |
#+-----------+----------------+-------------+-------------+---------+-------+-----------+------+-------+-----------+------------+---------+------------+----+------------------+
#| 305       | PF423H         |             | 02/01/2019  | Trailer | 23.79 | JV UK     | 2019 |     0 | Wednesday | AS5779     | PF      |          1 |  1 | 2019-01-02       |
#| 1227      | pf576h dehired |             | 02/01/2019  | Hired   | 23.79 | JV UK     | 2019 |     0 | Wednesday | 568890-TIP | PF      |          1 |  2 | 2019-01-02       |
#| 977       | PF726E         |             | 02/01/2019  | Trailer | 23.79 | JV APF    | 2019 |     0 | Wednesday | AS7154     | PF      |          1 |  3 | 2019-01-02       |
#| 804       | PF659E         |             | 02/01/2019  | Trailer | 23.79 | JV FRANCE | 2019 |     0 | Wednesday | AS6870     | PF      |          1 |  4 | 2019-01-02       |
#+-----------+----------------+-------------+-------------+---------+-------+-----------+------+-------+-----------+------------+---------+------------+----+------------------+


import mysql.connector
from config import configtw as cfg

class tw_transactionsDAO:
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
        self.database="truckwash"
    
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
    def getAll_(self): #this returns the native content of the query results
        cursor = self.getCursor()
        sql = "select * from tw_transactions limit 10"
        cursor.execute(sql)
        result = cursor.fetchall()
        self.closeAll()
        return result
    

    def getAll(self):
        cursor = self.getCursor()
        sql="select * from tw_transactions limit 100"
        cursor.execute(sql)
        result = cursor.fetchall()
        tw_transactionslist = []
        for row in result:
            tw_transactionslist.append(self.convertToDict(row))

        self.closeAll()
        return tw_transactionslist

    def findByID(self, id):
        cursor = self.getCursor()
        sql="select * from tw_transactions where id = %s"
        values = (id,)

        cursor.execute(sql, values)
        result = cursor.fetchone()
        self.closeAll()
        return self.convertToDict(result)
    
    def create(self, tw_transactions):
        cursor = self.getCursor()
        sql="insert into tw_transactions (name, age) values (%s,%s)"
        values = (tw_transactions.get("name"), tw_transactions.get("age"))
        cursor.execute(sql, values )

        self.connection.commit()
        newid = cursor.lastrowid
        tw_transactions["id"] = newid
        self.closeAll()
        return tw_transactions


    def update(self, id,  tw_transactions):
        cursor = self.getCursor()
        sql="update tw_transactions set name= %s, age=%s  where id = %s"
    
        values = (tw_transactions.get("name"), tw_transactions.get("age"), id)
        cursor.execute(sql, values)
        self.connection.commit()
        
        self.closeAll()
        return tw_transactions

    def delete(self, id):
        cursor = self.getCursor()
        sql="delete from tw_transactions where id = %s"
        values = (id,)

        cursor.execute(sql, values)

        self.connection.commit()
        self.closeAll
        #print("delete done")
        return True

    def convertToDict(self,resultLine):
        tw_transactionsKeys = [
        "MoveIT ID", "FleetNumber", "Third party", "source_Date",
        "EQ Type", "Rate", "JV", "Year", "Month", "Dayname",
        "Reg", "TP Code", "Weeknumber", "id", "Transaction_Date"
    ]
        currentkey = 0
        tw_transactions = {}
        for attrib in resultLine:
            tw_transactions[tw_transactionsKeys[currentkey]] = attrib
            currentkey = currentkey + 1 
        return tw_transactions

tw_transactionsDAO = tw_transactionsDAO()
