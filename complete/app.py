from re import A
import os
import sqlite3
from flask import Flask, render_template, request, flash, redirect, url_for, jsonify
from flask import send_from_directory
from werkzeug.utils import secure_filename
import sqlite3

app = Flask(__name__, static_folder="./templates/images")
app.secret_kry = "lock"


STATIC_FOLDER = "./templates/images"

ALLOWED_EXTENSIONS = set(["png", "jpg", "gif", "heic", "jpeg"])

app.config["STATIC_FOLDER"] = STATIC_FOLDER

if not os.path.exists(STATIC_FOLDER):
    os.makedirs(STATIC_FOLDER)

todo_db = sqlite3.connect("todos.db", check_same_thread=False)

types = [
    "None",
    "Submit",
    "Todo",
    "loop"
]


def allwed_file(filename):
    # .があるかどうかのチェックと、拡張子の確認
    # OKなら１、だめなら0
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["POST", "GET"])
def index():
    todo_lists = todo_db.execute("SELECT * FROM todos")
    return render_template("./index.html", todo_lists=todo_lists, types=types)


@app.route("/todo_insert", methods=["GET", "POST"])
def todo_insert():
    text_insert = request.form.get("text_insert")
    print(text_insert)
    type_text = request.form.get("type_text")
    print(type_text)
    todo_db.execute(
        "INSERT INTO todos(contents, type) VALUES(?, ?)", (text_insert, type_text))
    todo_db.commit()
    todo_lists = todo_db.execute("SELECT * FROM todos")
    return render_template("./index.html", todo_lists=todo_lists, types=types)


@app.route("/todo_delete", methods=["GET", "POST"])
def todo_delete():
    text_delete = request.form.get("text_delete")
    print(text_delete)
    todo_db.execute("DELETE FROM todos WHERE id = ?", (text_delete, ))
    todo_lists = todo_db.execute("SELECT * FROM todos")
    return render_template("./index.html", todo_lists=todo_lists, types=types)


@app.route("/todo_search_number", methods=["GET", "POST"])
def todo_search_number():
    id_todo_search = request.form.get("id_todo_search")
    print(id_todo_search)
    todo_limits = todo_db.execute(
        "SELECT * FROM todos WHERE id = ?", (id_todo_search,))
    return render_template("./search_number.html", todo_limits=todo_limits, types=types)


@app.route("/todo_search_text", methods=["GET", "POST"])
def todo_search_text():
    text_todo_search = request.form.get("text_todo_search")
    print(type(text_todo_search))
    todo_limits = todo_db.execute(
        "SELECT * FROM todos WHERE contents LIKE  ? ", (text_todo_search,))
    return render_template("./search_text.html", todo_limits=todo_limits)


@app.route("/todo_scraiping")
def todo_scraiping():
    return render_template("./scraiping.html")


@app.route("/loop_delete", methods=["GET", "POST"])
def loop_delete():
    loop_delete = request.form.get("btn_loop_delete")
    todo_db.execute("DELETE FROM todos WHERE id = ?", (loop_delete,))
    todo_db.commit()
    todo_lists = todo_db.execute("SELECT * FROM todos")
    return render_template("./index.html", todo_lists=todo_lists, types=types)


@app.route("/loop_open", methods=["GET", "POST"])
def loop_open():
    loop_open = request.form.get("btn_loop_open")
    print(loop_open)
    open_file = todo_db.execute(
        "SELECT contents FROM todos WHERE id = ?", (loop_open,))
    return render_template("./search_numbered.html", open_file=open_file, types=types)


@app.route("/file_open", methods=["GET", "POST"])
def file_open():
    file_open = request.form.get("btn_file_open")
    print(file_open)
    return "Hello"


@app.route("/todo_search_type", methods=["POST", "GET"])
def todo_search_type():
    search_type = request.form.get("search_type")
    print(search_type)
    todo_lists = todo_db.execute("SELECT * FROM todos")
    search_types = todo_db.execute("SELECT * FROM todos")
    return render_template("search_type.html", todo_lists=todo_lists, search_types=search_types)


@app.route("/option", methods=["POST"])
def option():
    delete_lists = todo_db.execute("SELECT * FROM todos")
    search_numbers = todo_db.execute("SELECT * FROM todos")
    search_texts = todo_db.execute("SELECT * FROM todos")
    search_types = todo_db.execute("SELECT * FROM todos")
    return render_template("./option.html", delete_lists=delete_lists, search_numbers=search_numbers, search_texts=search_texts, search_types=search_types)


@app.route("/uploads", methods=["POST"])
def uploads():
    filenames = todo_db.execute("SELECT * FROM filenames")
    return render_template("./uploads.html", filenames=filenames)


@app.route('/upload_page', methods=['GET', 'POST'])
def uploads_file():
    if request.method == 'POST':
        file = request.files['file']
        if not file:
            filenames = todo_db.execute("SELECT * FROM filenames")
            return render_template("./uploads.html", filenames=filenames)
        if file and allwed_file(file.filename):
            filename = secure_filename(file.filename)
            file_date = request.form.get("file_date")
            todo_db.execute("INSERT INTO filenames(contents, date) VALUES(?, ?)", (filename, file_date))
            todo_db.commit()
            filenames = todo_db.execute("SELECT * FROM filenames")
            file.save(os.path.join(app.config['STATIC_FOLDER'], filename))
            return render_template("uploads.html", filenames=filenames)
    return render_template("./uploads.html")


@app.route("/delete_uploads", methods=["POST", "GET"])
def delete_uploads():
    delete_upload_id = request.form.get("btn_delete_uploads")
    todo_db.execute("DELETE FROM filenames WHERE id = ?", (delete_upload_id,))
    todo_db.commit()
    filenames = todo_db.execute("SELECT * FROM filenames")
    return render_template("./uploads.html", filenames=filenames)


@app.route("/searched_type")
def searched_type():
    return "Hello"


@app.route("/board")
def board():
    filenames = todo_db.execute("SELECT * FROM filenames")    
    return render_template("./board.html", filenames=filenames)

if __name__ == "__main__":
    app.run(debug=True)
