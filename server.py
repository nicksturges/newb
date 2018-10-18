from flask import Flask, render_template, redirect, request

from mysqlconnection import connectToMySQL
import datetime
app = Flask(__name__)
# invoke the connectToMySQL function and pass it the name of the database we're using
# connectToMySQL returns an instance of MySQLConnection, which we will store in the variable 'mysql'
# mysql = connectToMySQL(' ')
# now, we may invoke the query_db method

def getBook():
    mysql = connectToMySQL("bookList")
    books = mysql.query_db("SELECT * FROM books")
    return books

def getBookById(id):
    mysql = connectToMySQL("bookList")
    query = "SELECT * FROM books WHERE id = %(id)s"
    data = {"id": id}
    books = mysql.query_db(query, data)
    return books[0]

def deleteBook(id):
    mysql = connectToMySQL("bookList")
    query = "DELETE FROM `email_db`.`books` WHERE (`id` = %(id)s);"
    data = {"id": id}
    book = mysql.query_db(query, data)
    return book

def addBookToDatabase(book):
    mysql = connectToMySQL("bookList")
    query = "INSERT INTO books (`title`, `author`, `description`, `created_at`) VALUES (%(title)s, %(author)s, %(description)s, %(created_at)s);"
    data = {
        "title": book["title"],
        "author": book["author"],
        "description": book["description"],
        "created_at": datetime.datetime.now()
    }
    book = mysql.query_db(query, data)
    return book

def editBookToDatabase(id,book):
    mysql = connectToMySQL("bookList")
    query = "UPDATE books SET `title` = %(title)s, `author` = %(author)s, WHERE (`id` = %(id)s);"
    data = {
        "title": book["title"],
        "author": book["author"],
        "description": book["description"],
        "created_at": datetime.datetime.now(),
        "id" : id
    }
    book = mysql.query_db(query, data)
    return book

@app.route('/')
def index():
    books = getBook()
    return render_template("index.html", books = books)

@app.route("/delete/<id>")
def delete(id):
    deleteBook(id)
    return redirect("/")

@app.route("/add")
def add():
    return render_template("add.html")

@app.route('/edit/<id>')
def edit(id):
    book = getBookById(id)
    return render_template("edit.html", book = book)

@app.route("/addBook", methods=["POST"])
def addBook():
    book = addBookToDatabase(request.form)
    return redirect("/")

@app.route("/editBook/<id>", methods=["POST"])
def editBook(id):
    book = editBookToDatabase(id, request.form)
    return redirect("/")




# print("all the users", mysql.query_db("SELECT * FROM Users;"))
if __name__ == "__main__":
    app.run(debug=True)