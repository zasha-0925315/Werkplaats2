import os.path

from flask import Flask, render_template, request, url_for, redirect, session

from lib.tablemodel import DatabaseModel
from lib.Login_details import Login_details

# Create the application.
LISTEN_ALL = "0.0.0.0"
FLASK_IP = LISTEN_ALL
FLASK_PORT = 81
FLASK_DEBUG = True
app = Flask(__name__)

# set the secret key
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
# This command creates the "<application directory>/databases/testcorrect_vragen.db" path
DATABASE_FILE = os.path.join(app.root_path, 'databases', 'testcorrect_vragen.db')

# Check if the database file exists.
if not os.path.isfile(DATABASE_FILE):
    print(f"Could not find database {DATABASE_FILE}, creating a demo database.")
dbm = DatabaseModel(DATABASE_FILE)


# checks on each screen if user is logged in, if not redirect to login page
@app.before_request
def before_request():
    if "user" not in session and request.endpoint not in ['login', 'static', 'login_index']:
        return redirect(url_for('login_index'))


# if logged in, show the home page, otherwise show the login page
@app.route("/")
def login_index():
    if "user" in session:
        return redirect(url_for('index'))
    else:
        session.pop('logged_in', None)
        return render_template('login.html')


# checks if username and password are correct, if so, redirect to home page
@app.route("/login", methods=['GET', 'POST'])
def login():
    # Check if the form was submitted
    if request.method == 'POST':
        Username = request.form.get('Username')
        Password = request.form.get('Password')
        # Check if the username and password are correct
        data = Login_details
        if Username in data:
            if Password == data[Username]:
                # If the username and password are correct, redirect to the main page
                session['user'] = Username
                return redirect(url_for('index'))
            else:
                # If the password is incorrect, return to the login page
                error = 'Gebruikersnaam of wachtwoord is incorrect'
                return render_template('login.html', error=error)
        else:
            # If the username is incorrect, return to the login page
            error = 'Gebruikersnaam of wachtwoord is incorrect'
            return render_template('login.html', error=error)


# This is the main route that shows the home page
@app.route("/home")
def index():
    tables = dbm.get_table_list()
    return render_template(
        "tables.html", table_list=tables, database_file=DATABASE_FILE, Username=session['user']
    )


# Redirects user to logout page and clears session
@app.route("/logout")
def logout():
    session.pop('user', None)
    return redirect('/')


# The table route displays the content of a table
@app.route("/table_details/<table_name>")
def table_content(table_name=None):
    if not table_name:
        return "Missing table name", 400  # HTTP 400 = Bad Request
    else:
        rows, column_names = dbm.get_table_content(table_name)
        return render_template(
            "table_details.html", rows=rows, columns=column_names, table_name=table_name
        )


@app.route("/table_details/<table_name>/<id>/update", methods=['GET', 'POST'])
def update(table_name, id):
    row, column_names = dbm.get_data(table_name, id)

    return render_template(
        "update.html", table_name=table_name, row=row
    )


# App Routes | Update function | Jordy Arjun Sharma

# 'Vragen' Page:
@app.route("/update/vraag", methods=['POST'])
def updatevraag():
    field = request.form['vraag']
    vragenleerdoel = request.form['vragen_leerdoel']
    vragenauteurs = request.form['vragen_auteur']
    id = request.form['id']
    dbm.update_vraag(field, id)
    dbm.update_leerdoel(vragenleerdoel, id)
    dbm.update_auteur(vragenauteurs, id)
    return redirect(url_for("table_content", table_name='vragen'))




# 'Leerdoelen' Page:
@app.route("/update/leerdoelen", methods=['POST'])
def updateleerdoel():
    edit_leerdoel = request.form['formleerdoel']
    leerdoel_id = request.form['leerdoelid']
    dbm.update_leerdoelen(edit_leerdoel, leerdoel_id)
    return redirect(url_for("table_content", table_name='leerdoelen'))


# 'Auteurs' Page:
@app.route("/update/auteurs", methods=['POST'])
def updateauteurs():
    auteurs_id = request.form['auteursid']
    edit_voornaam = request.form['voornaam']
    edit_achternaam = request.form['achternaam']
    edit_geboortejaar = request.form['geboortejaar']
    edit_medewerker = request.form['medewerker']
    dbm.update_auteurs(edit_voornaam, edit_achternaam, edit_geboortejaar, edit_medewerker, auteurs_id)
    return redirect(url_for("table_content", table_name='auteurs'))



@app.route("/table_details/<table_name>", methods=("POST", "GET"))
def table_filter(table_name=None):
    match table_name:
        case "auteurs" | "leerdoelen":
            selected_column = ""
            typed = ""
            between_typed = ""
            between_typed2 = ""
            data_type = ""
            way = ""

            if request.method == 'POST':
                selected_column = request.form['column_select']
                typed = request.form['typed']
                between_typed = request.form['between_typed']
                between_typed2 = request.form['between_typed2']
                data_type = request.form['data_type']
                way = request.form['way']

            rows, column_names = dbm.get_table_search(
                table_name,
                selected_column,
                typed,
                between_typed,
                between_typed2,
                data_type,
                way
            )
            return render_template(
                "table_details.html",
                rows=rows,
                columns=column_names,
                table_name=table_name,
                selected_column=selected_column
            )

        case "vragen":
            filter_name = ""
            if request.method == 'POST':
                filter_name = str(request.form['filter_name'])
            rows, column_names = dbm.get_table_filtered(table_name, filter_name)
            return render_template(
                "table_details.html", rows=rows, columns=column_names, table_name=table_name, filter_name=filter_name
            )

@app.route("/table_details/<table_name>/<id>/delete", methods=['POST', 'GET', 'DELETE'])
def delete(table_name, id):
    dbm.delete(table_name, id)


    return render_template(
        "delete.html", table_name=table_name
    )


if __name__ == "__main__":
    app.run(host=FLASK_IP, port=FLASK_PORT, debug=FLASK_DEBUG)
