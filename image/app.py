from flask import Flask, render_template
import sqlite3

app = Flask(__name__, static_folder='./templates/images')

todo_db = sqlite3.connect("todos.db", check_same_thread=False)


@app.route("/", methods=["POST", "GET"])
def index():
    temp = todo_db.execute("SELECT * FROM todos")
    return render_template("./index.html", temp=temp)


if __name__ == "__main__":
    app.run(debug=True)
