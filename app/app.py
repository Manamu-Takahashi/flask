from flask import Flask, render_template, request, flash
import sqlite3


app = Flask(__name__)

db = sqlite3.connect("todos.db", check_same_thread=False)


@app.route("/")
def index():
    todos = db.execute("SELECT * FROM todos")
    return render_template("./index.html", todos=todos)


@app.route("/insert")
def insbtn():
    todos = db.execute("SELECT * FROM todos")
    return render_template("./insert.html", todos=todos)


@app.route("/delete")
def dltbtn():
    todos = db.execute("SELECT * FROM todos")
    return render_template("./delete.html", todos=todos)


@app.route("/inserted", methods=["GET", "POST"])
def insdbtn():
    contests = request.form.get("contents")
    if not contests:
        return render_template("./index.html")

    db.execute('INSERT INTO todos (contents) VALUES(?)', (contests, ))
    db.commit()
    
    todos = db.execute("SELECT * FROM todos")

    return render_template("./insert.html", todos=todos)


@app.route("/deleted", methods=["GET", "POST"])
def dltdbtn():
    number = request.form.get("number")
    if not number:
        return render_template("./index.html")

    db.execute('DELETE FROM todos WHERE id = ?', (number, ))
    db.commit()

    todos = db.execute("SELECT * FROM todos")

    return render_template("./delete.html", todos=todos)


@app.route("/back")
def back():
    todos = db.execute("SELECT * FROM todos")
    return render_template("./index.html", todos=todos)


#rd button not complete
@app.route("/rdbtn")
def rdbtn():
    todos = db.execute("SELECT * FROM todos")

    idbtn = request.form.get("idbtn")
    print(idbtn)

    delete = db.execute("DELETE FROM todos WHERE id = ?", (idbtn, ))
    db.commit()

    return render_template("./index.html", todos=todos)

@app.route("/serch")
def serch():
    return ""


if __name__ == "__main__":
    app.run(debug=True)