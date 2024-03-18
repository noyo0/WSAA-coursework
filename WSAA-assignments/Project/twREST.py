# create a very simple Flask server
# API fuinctions (HTML method): Get All (GET), Find by ID (GET), Create Book (POST), Update Book (PUT), Delete Book (DELETE)

from flask import Flask, request #import library and functions
# Flask port is 5000 http://localhost:5000 or http://127.0.0.1:5000
app = Flask(__name__) #initialise Flask Application

# INDEX - define route for the index page
@app.route('/')
# define index content
def index():
        return """<h1> ******  Truckwash_SQL INDEX ******* </h1><br>
        <h2>CONTENTS:</h2>
                http://localhost:5000 - INDEX<br>
                http://localhost:5000/transactions - All transactions<br>
                http://localhost:5000/transactions/1 - transactions by ID<br>
<br>
                new item:<br>
                (POST) http://localhost:5000/transactions - creates new item<br>
                        JSON template<br>
                        {<br>
                        "Fleet number":"PF123",<br>
                        "type":"truck",<br>
                        "price":123,<br>
                        "date":"01/03/24"<br>
                        }<br>
<br>
                edit item:<br>
                http://localhost:5000/transactions/1 - edit by ID<br>
                        JSON template<br>
                        {<br>
                        "Fleet number":"PF123",<br>
                        "type":"truck",<br>
                        "price":123,<br>
                        "date":"01/03/24"<br>
                        }<br>
<br>
                """
# cURL command: http://127.0.0.1:5000/transactions
@app.route('/transactions', methods=['GET']) #GET reads
def getall():
        return "Here you get all truckwash transactions"

# Find transaction by ID: Define a route to handle GET requests for finding a book by its ID.
# cURL command: http://127.0.0.1:5000/transactions/1
@app.route('/transactions/<int:id>', methods=['GET']) #GET reads
def findbyid(id):
        return "Here you can find a particular transaction by ID"

# Create transaction: Define a route to handle POST requests for creating a new book entry.
# cURL command: -X POST -d 
# JSON template to send {"Fleet number":"PF123", "type":"truck", "price":123, "date":"01/03/24"}
# address http://127.0.0.1:5000/transactions
@app.route('/transactions', methods=['POST']) #POST creates
def create():
        # read json from the body
        jsonstring = request.json
        return f"create {jsonstring}"

# Update transaction: Define a route to handle PUT requests for updating an existing entry
# cURL command: -X PUT -d "{"Fleet number":"PF123", "type":"truck", "price":123, "date":"01/03/24"}" http://127.0.0.1:5000/transactions/1
@app.route('/transactions/<int:id>', methods=['PUT']) #PUT updates
def update(id):
        jsonstring = request.json
        return f"update {id} {jsonstring}"

# Delete Book: Define a route to handle DELETE requests for deleting a book by its ID.
# cURL command: -X DELETE  http://127.0.0.1:5000/transactions/1
@app.route('/transactions/<int:id>', methods=['DELETE']) #DELETE
def delete(id):
        return f"delete {id}"

# Run the Flask application in debug mode if the script is executed directly.
if __name__ == "__main__":
    app.run(debug = True)