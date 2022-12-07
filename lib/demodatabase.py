import sqlite3

dbFile = 'mydb.db'
dbTable = 'login'
user = 'jelle'
password = 'mijn_wachtwoord2'
dbConnection = sqlite3.connect("dbFile")
cursor = dbConnection.cursor()

query = 'CREATE TABLE IF NOT EXISTS {} (username TEXT, password TEXT);'.format(dbTable)
cursor.execute(query)

query = 'INSERT INTO {} VALUES ("{}", "{}");'.format(dbTable, user, password)
cursor.execute(query)

query = 'SELECT * FROM {};'.format(dbTable)
result = cursor.execute(query)

dbConnection.commit()
print(result.fetchone())
