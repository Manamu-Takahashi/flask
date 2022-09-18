#Flaskとrender_template（HTMLを表示させるための関数）をインポート
from flask import Flask, render_template, request, flash
import sqlite3



#Flaskオブジェクトの生成
app = Flask(__name__)

db = sqlite3.connect("todos.db", check_same_thread=False)


#「/」へアクセスがあった場合に、"Hello World"の文字列を返す
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

#おまじない
if __name__ == "__main__":
    app.run(debug=True)