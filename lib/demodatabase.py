import sqlite3

def create_login_database(login_database_file):
    try:
        connection = sqlite3.connect(login_database_file)
    cursor = connection.cursor()

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS demo (id PRIMARY KEY, username TEXT,password TEXT)"
    )

    for pair in [
        ("Veysel", "Altinok", "v.k.altinok@hr.nl"),
        ("Diederik", "de Vries", "d.de.vries@hr.nl"),
        ("Mark", "Otting", "m.b.otting@hr.nl"),
    ]:
        cursor.execute(
            "INSERT INTO demo (first_name, last_name, email) VALUES (?, ?, ?)", pair
        )
    connection.commit()
    connection.close()
