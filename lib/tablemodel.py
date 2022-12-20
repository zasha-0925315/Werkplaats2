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
        cursor.execute(f"SELECT * FROM {table_name}")
        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        # Note that this method returns 2 variables!
        return table_content, table_headers

    def get_table_filtered(self, table_name, filter_name):
        cursor = sqlite3.connect(self.database_file).cursor()

        match filter_name:
            case "wrong_leerdoelen":
                cursor.execute(f"SELECT * FROM {table_name} "
                               f"WHERE leerdoel NOT IN (SELECT id FROM leerdoelen)")
            case "wrong_auteurs":
                cursor.execute(f"SELECT * FROM {table_name} "
                               f"WHERE auteur NOT IN (SELECT id FROM auteurs)")
            case "html_system_codes":
                cursor.execute(f"SELECT * FROM {table_name} "
                               f"WHERE vraag LIKE '%<br>%' OR vraag LIKE '%&nbsp;%' OR vraag LIKE '%¤%'")
            case "empty_rows":
                cursor.execute(f"SELECT * FROM {table_name} "
                               f"WHERE leerdoel IS NULL OR auteur IS NULL;")
            case "full_rows":
                cursor.execute(f"SELECT * FROM {table_name} "
                               f"WHERE leerdoel IS NOT NULL OR auteur IS NOT NULL;")

        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchall()

        # Note that this method returns 2 variables!
        return table_content, table_headers

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
                cursor.execute(f"SELECT * FROM {table_name} "
                               f"WHERE {selected_column} LIKE '%{typed}%'")
            case "is_not":
                cursor.execute(f"SELECT * FROM {table_name} "
                               f"WHERE {selected_column} IS NOT {typed}")
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

    # def update(self):
    #     cursor = sqlite3.connect(self.database_file).cursor()
    #     cursor.execute("UPDATE vragen SET vraag='' WHERE id='' ")
    #
    #     # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
    #     table_headers = [column_name[0] for column_name in cursor.description]
    #     table_content = cursor.fetchall()
    #
    #     # Note that this method returns 2 variables!
    #     return table_content, table_headers



    def get_data(self, table_name, id):
        cursor = sqlite3.connect(self.database_file).cursor()
        cursor.execute(f"SELECT * FROM {table_name} WHERE id={id} ")
        # An alternative for this 2 var approach is to set a sqlite row_factory on the connection
        table_headers = [column_name[0] for column_name in cursor.description]
        table_content = cursor.fetchone()

        # Note that this method returns 2 variables!
        return table_content, table_headers


    def update_vraag(self, field, id):
        cursor = sqlite3.connect(self.database_file)
        cursor.execute(f''' UPDATE vragen SET vraag='{field}' WHERE id='{id}' ;''')
        cursor.commit()

    def update_leerdoel(self, vragenleerdoel, id):
        cursor = sqlite3.connect(self.database_file)
        cursor.execute(f''' UPDATE vragen SET leerdoel='{vragenleerdoel}' WHERE id='{id}' ;''')
        cursor.commit()

    def update_auteur(self, vragenauteurs, id):
        cursor = sqlite3.connect(self.database_file)
        cursor.execute(f''' UPDATE vragen SET auteur='{vragenauteurs}' WHERE id='{id}' ;''')
        cursor.commit()

    # def vragen_auteur(self, leerdoelform, id):
    #     cursor = sqlite3.connect(self.database_file)
    #     cursor.execute(f''' UPDATE vragen SET leerdoel='{leerdoelform}' WHERE id='{id}' ;''')
    #     cursor.commit()