# create a very simple Flask server
# API fuinctions (HTML method): Get All (GET), Find by ID (GET), Create Book (POST), Update Book (PUT), Delete Book (DELETE)

from flask import Flask, request #import library and functions

app = Flask(__name__) #initialise Flask Application

# INDEX - define route for the index page
@app.route('/')
# define index content
def index():
        return "Hello world 04/03/24_19:00"

# GET All Books: Define a route to handle GET requests for retrieving all books.https://jsonplaceholder.typicode.com/posts/1
# cURL command: http://127.0.0.1:5000/books
@app.route('/books', methods=['GET']) #GET reads
def getall():
        return "Here you get all the books"

# Find Book by ID: Define a route to handle GET requests for finding a book by its ID.
# cURL command: http://127.0.0.1:5000/books/1
@app.route('/books/<int:id>', methods=['GET']) #GET reads
def findbyid(id):
        return "Here you can find a particular book by ID"

# Create Book: Define a route to handle POST requests for creating a new book entry.
# cURL command: -X POST -d 
# JSON template to send {"title":"test", "author":"some guy", "price":123}
# address http://127.0.0.1:5000/books
@app.route('/books', methods=['POST']) #POST creates
def create():
        # read json from the body
        jsonstring = request.json
        return f"create {jsonstring}"

# Update Book: Define a route to handle PUT requests for updating an existing book entry
# cURL command: -X PUT -d "{\"title\":\"test\", \"author\":\"some guy\", \"price\":123}" http://127.0.0.1:5000/books/1
@app.route('/books/<int:id>', methods=['PUT']) #PUT updates
def update(id):
        jsonstring = request.json
        return f"update {id} {jsonstring}"

# Delete Book: Define a route to handle DELETE requests for deleting a book by its ID.
# cURL command: -X DELETE  http://127.0.0.1:5000/books/1
@app.route('/books/<int:id>', methods=['DELETE']) #DELETE
def delete(id):
        return f"delete {id}"

# Run the Flask application in debug mode if the script is executed directly.
if __name__ == "__main__":
    app.run(debug = True)