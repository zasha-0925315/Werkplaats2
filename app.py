import os.path
import sys

from flask import Flask, render_template, redirect, url_for, request

from lib.tablemodel import DatabaseModel
from lib.filters import filters

# This demo glues a random database and the Flask framework. If the database file does not exist,
# a simple demo dataset will be created.
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True

app = Flask(__name__)
# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
DATABASE_FILE = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')

# Check if the database file exists. If not, create a demo database
if not os.path.isfile(DATABASE_FILE):
    print(f"Could not find database {DATABASE_FILE}")
dbm = DatabaseModel(DATABASE_FILE)

# Main route that shows a list of tables in the database
# Note the "@app.route" decorator. This might be a new concept for you.
# It is a way to "decorate" a function with additional functionality. You
# can safely ignore this for now - or look into it as it is a really powerful
# concept in Python.

@app.route("/")
def login_index():
    return render_template(
    "login.html"
    )

# Route for handling the login page logic
@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'hoi' or request.form['password'] != '123':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route("/home")
def index():
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE_FILE
    )

# The table route displays the content of a table
@app.route("/table_details/<table_name>")
def table_content(table_name=None):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        filter_list = filters
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "table_details.html", rows=rows, columns=column_names, table_name=table_name, filter_list=filter_list
        )
@app.route("/table_details/<table_name>/<filter_name>")
def table_filter(table_name=None, filter_name=None):

    rows, column_names = dbm.get_table_filtered(table_name, filter_name)
    return render_template(
        "table_details.html",rows=rows, columns=column_names, table_name=table_name
    )

if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
