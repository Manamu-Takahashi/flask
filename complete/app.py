import sqlite3
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

todo_db = sqlite3.connect("todos.db", check_same_thread=False)

@app.route("/")
def index():
    return render_template("./index.html")

@app.route("/todo_insert", methods=["GET", "POST"])
def todo_insert():
    text_insert = request.form.get("text_insert")
    print(text_insert)
    todo_db.execute("INSERT INTO todos(text) VALUES(?)", (text_insert,))
    todo_db.commit()
    return "todo_insert"

@app.route("/todo_delete")
def todo_delete():
    return "todo_delete"


if __name__ == "__main__":
    app.run(debug=True)
