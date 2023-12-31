import os
import sqlite3


class DatabaseModel:
    """This class is a wrapper around the sqlite3 database. It provides a simple interface that maps methods
    to database queries. The only required parameter is the database file."""

    def __init__(self, database_file):
        self.database_file = database_file
        if not os.path.exists(self.database_file):
            raise FileNotFoundError(f"Could not find database file: {database_file}")

    # Using the built-in sqlite3 system table, return a list of all tables in the database
    def get_table_list(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [table[0] for table in cursor.fetchall()]
        return tables

    # Given a table name, return the rows and column names
    def get_table_content(self, table_name):
        cursor = sqlite3.connect(self.database_file).cursor()

        # a match to give the possibility to change the standard query to something specific depending on the table
        match table_name:
            case "vragen":
                cursor.execute(f"SELECT vragen.id, leerdoelen.leerdoel, vraag, "
                               f"(auteurs.voornaam || ' ' || auteurs.achternaam) "
                               f"FROM vragen "
                               f"LEFT JOIN leerdoelen on vragen.leerdoel = leerdoelen.id "
                               f"LEFT JOIN auteurs on vragen.auteur = auteurs.id ")
            case _:
                cursor.execute(f"SELECT * FROM {table_name}")

        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        # Note that this method returns 2 variables!
        return table_content, table_headers

    # the function to change the shown row in the table depending on the selected filter
    def get_table_filtered(self, filter_name):
        cursor = sqlite3.connect(self.database_file).cursor()

        match filter_name:
            case "wrong_leerdoelen":
                cursor.execute(f"SELECT vragen.id, leerdoelen.leerdoel, vraag, "
                               f"(auteurs.voornaam || ' ' || auteurs.achternaam) "
                               f"FROM vragen "
                               f"LEFT JOIN leerdoelen on vragen.leerdoel = leerdoelen.id "
                               f"LEFT JOIN auteurs on vragen.auteur = auteurs.id "
                               f"WHERE vragen.leerdoel NOT IN (SELECT id FROM leerdoelen)")
            case "wrong_auteurs":
                cursor.execute(f"SELECT vragen.id, leerdoelen.leerdoel, vraag, "
                               f"(auteurs.voornaam || ' ' || auteurs.achternaam) "
                               f"FROM vragen "
                               f"LEFT JOIN leerdoelen on vragen.leerdoel = leerdoelen.id "
                               f"LEFT JOIN auteurs on vragen.auteur = auteurs.id "
                               f"WHERE auteur NOT IN (SELECT id FROM auteurs)")
            case "html_system_codes":
                cursor.execute(f"SELECT vragen.id, leerdoelen.leerdoel, vraag, "
                               f"(auteurs.voornaam || ' ' || auteurs.achternaam) "
                               f"FROM vragen "
                               f"LEFT JOIN leerdoelen on vragen.leerdoel = leerdoelen.id "
                               f"LEFT JOIN auteurs on vragen.auteur = auteurs.id "
                               f"WHERE vraag LIKE '%<br>%' OR vraag LIKE '%&nbsp;%' OR vraag LIKE '%¤%'")
            case "empty_rows":
                cursor.execute(f"SELECT vragen.id, leerdoelen.leerdoel, vraag, "
                               f"(auteurs.voornaam || ' ' || auteurs.achternaam) "
                               f"FROM vragen "
                               f"LEFT JOIN leerdoelen on vragen.leerdoel = leerdoelen.id "
                               f"LEFT JOIN auteurs on vragen.auteur = auteurs.id "
                               f"WHERE leerdoelen.leerdoel IS NULL OR vragen.auteur IS NULL;")
            case "full_rows":
                cursor.execute(f"SELECT vragen.id, leerdoelen.leerdoel, vraag, "
                               f"(auteurs.voornaam || ' ' || auteurs.achternaam) "
                               f"FROM vragen "
                               f"LEFT JOIN leerdoelen on vragen.leerdoel = leerdoelen.id "
                               f"LEFT JOIN auteurs on vragen.auteur = auteurs.id "
                               f"WHERE leerdoelen.leerdoel IS NOT NULL AND vragen.auteur IS NOT NULL;")

        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        # Note that this method returns 2 variables!
        return table_content, table_headers

    # the function to search for something specific in the table
    def get_table_search(self, table_name, selected_column, typed, between_typed, between_typed2, data_type, way):
        cursor = sqlite3.connect(self.database_file).cursor()

        data_type_query = ""

        match data_type:
            case "boolean":
                data_type_query = f"WHERE {selected_column} IS NOT '0' AND {selected_column} IS NOT '1'"
            case "date_1900":
                data_type_query = f"WHERE {selected_column} < 1900"

        match way:
            case "like":
                # cursor.execute(f"SELECT * FROM ? WHERE ? LIKE ?", [table_name, selected_column, typed])
                cursor.execute(f"SELECT * FROM {table_name} "
                               f"WHERE {selected_column} LIKE '%{typed}%'")
            case "is_not":
                cursor.execute(f"SELECT * FROM {table_name} "
                               f"WHERE {selected_column} NOT LIKE '%{typed}%'")
            case "between":
                cursor.execute(f"SELECT * FROM {table_name} "
                               f"WHERE {selected_column} BETWEEN {between_typed} AND {between_typed2}")
            case "wrong_data_type":
                cursor.execute(f"SELECT * FROM {table_name} "
                               f"{data_type_query}")
                print(data_type_query)

        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        # Note that this method returns 2 variables!
        return table_content, table_headers

    # function to select a single row
    def get_data(self, table_name, table_id):
        cursor = sqlite3.connect(self.database_file).cursor()
        if table_name == 'vragen':
            cursor.execute(f"SELECT * FROM vragen INNER JOIN leerdoelen ON vragen.leerdoel = leerdoelen.id")

        cursor.execute(f"SELECT * FROM {table_name} WHERE id={table_id}")

        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchone()

        # Note that this method returns 2 variables!
        return table_content, table_headers

    # function to get the id and leerdoel for showing them in de vragen table
    def get_list_leerdoelen(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT id, leerdoel FROM leerdoelen")

        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        # Note that this method returns 2 variables!
        return table_content, table_headers

    # function to get the id and full names of the auteurs for showing them in de vragen table
    def get_list_auteurs(self):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT id, (voornaam || ' ' || achternaam) FROM auteurs")

        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        # Note that this method returns 2 variables!
        return table_content, table_headers

# HERE ARE THE SQL QUERIES OF THE UPDATE FUNCTION
    # UPDATE QUERIES 'VRAGEN' PAGE:
    def update_vraag(self, field, table_id):
        cursor = sqlite3.connect(self.database_file)
        cursor.execute(f''' UPDATE vragen SET vraag='{field}' WHERE id='{table_id}' ;''')
        cursor.commit()

    def update_leerdoel(self, vragenleerdoel, table_id):
        cursor = sqlite3.connect(self.database_file)
        cursor.execute(f''' UPDATE vragen SET leerdoel='{vragenleerdoel}' WHERE id='{table_id}' ;''')
        cursor.commit()

    def update_auteur(self, vragenauteurs, table_id):
        cursor = sqlite3.connect(self.database_file)
        cursor.execute(f''' UPDATE vragen SET auteur='{vragenauteurs}' WHERE id='{table_id}' ;''')
        cursor.commit()

    # UPDATE QUERY 'LEERDOELEN' PAGE:
    def update_leerdoelen(self, edit_leerdoel, leerdoel_id):
        cursor = sqlite3.connect(self.database_file)
        cursor.execute(f'''UPDATE leerdoelen SET leerdoel='{edit_leerdoel}' WHERE id='{leerdoel_id}'; ''')
        cursor.commit()

    # UPDATE QUERIES 'AUTEURS' PAGE:
    def update_auteurs(self, edit_voornaam, edit_achternaam, edit_geboortejaar, edit_medewerker, auteurs_id):
        cursor = sqlite3.connect(self.database_file)
        cursor.execute(f''' UPDATE auteurs SET voornaam='{edit_voornaam}' WHERE id='{auteurs_id}' ;''')
        cursor.execute(f''' UPDATE auteurs SET achternaam='{edit_achternaam}' WHERE id='{auteurs_id}' ;''')
        cursor.execute(f''' UPDATE auteurs SET geboortejaar='{edit_geboortejaar}' WHERE id='{auteurs_id}' ;''')
        cursor.execute(f''' UPDATE auteurs SET medewerker='{edit_medewerker}' WHERE id='{auteurs_id}' ;''')
        cursor.commit()

    # function to delete a question
    def delete(self, table_name, table_id):
        db = sqlite3.connect(self.database_file)
        cursor = db.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE id={table_id}")
        db.commit()
