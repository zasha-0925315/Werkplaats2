import sqlite3

connection = sqlite3.connect("login.db")
cursor = connection.cursor()

cursor.execute(
    "CREATE TABLE login (username TEXT, password TEXT)"
    )

for login_list in [
    ("Jelle1", "ABC"),
    ("Jelle2", "123")
]:
    cursor.executemany(
        "INSERT INTO login VALUES (?, ?)", [login_list]
    )

    connection.commit()
connection.close()
