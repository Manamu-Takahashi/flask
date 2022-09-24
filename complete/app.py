from re import A
import sqlite3
from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

todo_db = sqlite3.connect("todos.db", check_same_thread=False)


@app.route("/")
def index():
    todo_lists = todo_db.execute("SELECT * FROM todos")
    return render_template("./index.html", todo_lists=todo_lists)


@app.route("/todo_insert", methods=["GET", "POST"])
def todo_insert():
    text_insert = request.form.get("text_insert")
    print(text_insert)
    todo_db.execute("INSERT INTO todos(contents) VALUES(?)", (text_insert,))
    todo_db.commit()
    todo_lists = todo_db.execute("SELECT * FROM todos")
    return render_template("./index.html", todo_lists=todo_lists)


@app.route("/todo_delete", methods=["GET", "POST"])
def todo_delete():
    text_delete = request.form.get("text_delete")
    print(text_delete)
    todo_db.execute("DELETE FROM todos WHERE id = ?", (text_delete, ))
    todo_lists = todo_db.execute("SELECT * FROM todos")
    return render_template("./index.html", todo_lists=todo_lists)


@app.route("/todo_search_number", methods=["GET", "POST"])
def todo_search_number():
    id_todo_search = request.form.get("id_todo_search")
    print(id_todo_search)
    todo_limits = todo_db.execute("SELECT * FROM todos WHERE id = ?", (id_todo_search,))
    return render_template("./search_number.html", todo_limits=todo_limits)


@app.route("/todo_search_text", methods=["GET", "POST"])
def todo_search_text():
    text_todo_search = request.form.get("text_todo_search")
    print(type(text_todo_search))
    todo_limits = todo_db.execute("SELECT * FROM todos WHERE contents LIKE  ? ", (text_todo_search,))
    return render_template("./search_text.html", todo_limits=todo_limits)


@app.route("/todo_scraiping")
def todo_scraiping():
    return render_template("./scraiping.html")


@app.route("/loop_delete", methods=["GET", "POST"])
def loop_delete():
    loop_delete = request.form.get("btn_loop_delete")
    todo_db.execute("DELETE FROM todos WHERE id = ?", (loop_delete,))
    todo_lists = todo_db.execute("SELECT * FROM todos")
    return render_template("./index.html", todo_lists=todo_lists)


@app.route("/loop_open", methods=["GET", "POST"])
def loop_open():
    loop_open = request.form.get("btn_loop_open")
    print(loop_open)
    open_file = todo_db.execute("SELECT contents FROM todos WHERE id = ?", (loop_open,))
    return render_template("./search_numbered.html", open_file=open_file)


@app.route("/file_open", methods=["GET", "POST"])
def file_open():
    file_open = request.form.get("btn_file_open")
    print(file_open)
    return "Hello"


if __name__ == "__main__":
    app.run(debug=True)
