import sqlite3
import typing
import itertools
from Models.models import *


class WorkspaceData:
    def __init__(self):
        self.conn = sqlite3.connect("database.db")
#        self.conn = sqlite3.connect('C:\\Users\\therog\\Desktop\\database.db')
        self.conn.row_factory = sqlite3.Row  # Makes the data retrieved from the database accessible by their column name
        self.cursor = self.conn.cursor()

        self.cursor.execute("CREATE TABLE IF NOT EXISTS users (username TEXT, usermail TEXT,"
                            " userpwd TEXT, userquestion TEXT, answerquestion TEXT)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS pedigrees (nombre_cachorro TEXT, sexo TEXT,"
                            " color TEXT, nacimiento TEXT, raza TEXT, criador TEXT, afijo_madre TEXT,"
                            " afijo_padre TEXT, nombre_madre TEXT, nombre_padre TEXT, propietario TEXT,"
                            " direccion TEXT, distrito TEXT, telefono TEXT, dni TEXT, certificado_code REAL,"
                            " genealogia_data TEXT, propietario_afijo TEXT, homologacion TEXT,"
                            " created_by TEXT, time_creation TEXT, chip_code TEXT)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS clientes (propietario TEXT, cliente_afijo TEXT,"
                            " direccion TEXT, distrito TEXT, telefono TEXT, dni TEXT, auto_cliente TEXT)")

        self.cursor.execute("CREATE TABLE IF NOT EXISTS app_data (cant_afijos_hoy TEXT, fecha_ultimo_afijo TEXT,"
                            " app_id TEXT)")

        self.conn.commit()  # Saves the changes

    def save(self, table: str, data: typing.List[typing.Tuple]):

        """
        Erase the previous table content and record new data to it.
        :param table: The table name
        :param data: A list of tuples, the tuples elements must be ordered like the table columns
        :return:
        """

        self.cursor.execute(f"DELETE FROM {table}")

        table_data = self.cursor.execute(f"SELECT * FROM {table}")

        columns = [description[0] for description in table_data.description]  # Lists the columns of the table

        # Creates the SQL insert statement dynamically
        sql_statement = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"

        self.cursor.executemany(sql_statement, data)
        self.conn.commit()
        self.cursor.close()

    # Users

    def check_login(self, email, pwd):

        t = (email,)
        self.cursor.execute('SELECT * FROM users WHERE usermail=?', t)
        new_data = self.cursor.fetchall()

        self.cursor.close()

        if len(new_data) == 0:
            return False

        if new_data[0]["userpwd"] == pwd:
            return True

        else:
            return False

    def register(self, table, user_data):

        #        self.cursor.execute(f"DELETE FROM {table}")
        detail = "none"
        try:

            # Check if Mail is already in use.
            check_mail_exist = self.get_single_element_data("users", "usermail", user_data[0][1])
            if len(check_mail_exist) == 1:
                # exists cant be created.
                detail = "mail_in_use"
                return False, detail

            table_data = self.cursor.execute(f"SELECT * FROM {table}")

            columns = [description[0] for description in table_data.description]  # Lists the columns of the table

            # Creates the SQL insert statement dynamically
            sql_statement = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"

            self.cursor.executemany(sql_statement, user_data)
            self.conn.commit()
            detail = "success"
            return True, detail
        except sqlite3.IntegrityError:
            detail = "error"
            return False, detail

    def reset_pwd(self, email, question, answerquestion, newpass):
        print("Recuperando PWD")
        print("mail: " + str(email))
        print("question: " + str(question))
        print("answer: " + str(answerquestion))
        print("new pass: " + str(newpass))

        t = (email,)
        self.cursor.execute('SELECT * FROM users WHERE usermail=?', t)
        new_data = self.cursor.fetchall()

        if len(new_data) == 0:
            # Cuenta no registrada.
            return "no_existe"

        if new_data[0]["userquestion"] == question and new_data[0]["answerquestion"] == answerquestion:
            # Se resetea la contraseña.
            self.cursor.execute("UPDATE users SET userpwd=? WHERE usermail=?", (newpass, email))
            self.conn.commit()
            return "exito"
        else:
            return "bad_data"

    # Add Data

    def add_new_certificado(self, table, new_certificado):
        table_data = self.cursor.execute(f"SELECT * FROM {table}")

        columns = [description[0] for description in table_data.description]  # Lists the columns of the table

        # Creates the SQL insert statement dynamically
        sql_statement = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"

        self.cursor.executemany(sql_statement, new_certificado)
        self.conn.commit()

    def add_new_cliente(self, table, new_cliente):
        table_data = self.cursor.execute(f"SELECT * FROM {table}")

        columns = [description[0] for description in table_data.description]  # Lists the columns of the table

        # Creates the SQL insert statement dynamically
        sql_statement = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"

        self.cursor.executemany(sql_statement, new_cliente)
        self.conn.commit()

    # Get Data

    def get(self, table: str) -> typing.List[sqlite3.Row]:

        """
        Get all the rows recorded for the table.
        :param table: The table name to get the rows from. e.g: strategies, watchlist
        :return: A list of sqlite3.Rows accessible like Python dictionaries.
        """

        self.cursor.execute(f"SELECT * FROM {table}")
        data = self.cursor.fetchall()

        return data

    def get_single_pedigree_data(self, pedigree_code):
        t = (pedigree_code,)
        self.cursor.execute('SELECT * FROM pedigrees WHERE certificado_code=?', t)
        new_data = self.cursor.fetchall()
        return new_data

    def get_single_element_data(self, table, filter_table, elemento_buscar):
        t = (elemento_buscar,)
        self.cursor.execute(f'SELECT * FROM {table} WHERE {filter_table}=?', t)
        new_data = self.cursor.fetchall()
        return new_data

    def get_max_cert_code(self):
        self.cursor.execute("SELECT MAX(certificado_code) AS maximum FROM pedigrees")

        result = self.cursor.fetchall()
        maximum = 0

#        print("leng: " + str(len(result)))
#        print(result[0][0])
        if result[0][0] is not None:

            for i in result:
                maximum = int(i[0])

        return maximum

    def get_data_multiple_filters(self, table, dict_filters, filters_str):
        list_of_results = []
        counter = 0
        # Execute multiple querys
        for key in dict_filters:
            t = (filters_str[counter],)
            print("checking: " + key)
            print("current counter: " + str(counter))
            if dict_filters[key] == 1:
                print("--------------")
                print("quering: " + table + "/" + key + "/" + filters_str[counter])
                self.cursor.execute(f'SELECT * FROM {table} WHERE {key}=?', t)
                new_data = self.cursor.fetchall()
                if len(new_data) > 0:
                    list_of_results.append(new_data)
                    print(type(new_data))
                    print(len(new_data))

            counter += 1

        # Join all list

        print("RESULTS")
        print("lists_size: " + str(len(list_of_results)))

        print("lists jointed")
        result = sum(list_of_results, [])
        print((len(result)))

        # filter data
        for element in result:
            print(element["certificado_code"])

        new_k = []
        for elem in result:
            if elem not in new_k:
                new_k.append(elem)
        result = new_k

        print("After cleaning")
        for element in result:
            print(element["certificado_code"])

        return result

    def get_data_clientes_filters(self, table, dict_filters, filters_str):
        list_of_results = []
        counter = 0
        # Execute multiple querys
        for key in dict_filters:
            t = (filters_str[counter],)
            print("key: " + key + "/value: " + str(dict_filters[key]))
            if dict_filters[key] == 1 and key != "raza":
                print("quering: " + table + "/" + key + "/" + filters_str[counter])
                self.cursor.execute(f'SELECT * FROM {table} WHERE {key}=?', t)
                new_data = self.cursor.fetchall()
                if len(new_data) > 0:
                    list_of_results.append(new_data)
                    print(type(new_data))
                    print(len(new_data))

            counter += 1

        if filters_str[-1] != "Raza":
            if dict_filters["raza"] == 1:
                t = (filters_str[-1],)  # raza
                self.cursor.execute(f'SELECT * FROM "pedigrees" WHERE raza=?', t)
                all_raza_match = self.cursor.fetchall()

                for row in all_raza_match:
                    current_cliente_afijo = row[17]
                    cliente = (current_cliente_afijo,)
                    self.cursor.execute('SELECT * FROM clientes WHERE cliente_afijo=?', cliente)
                    cliente_data = self.cursor.fetchall()
                    list_of_results.append(cliente_data)

        # Join all list

        print("RESULTS")
        print("lists_size: " + str(len(list_of_results)))

        print("lists jointed")
        result = sum(list_of_results, [])
        print((len(result)))

        # filter data
        for element in result:
            print(element["cliente_afijo"])

        new_k = []
        for elem in result:
            if elem not in new_k:
                new_k.append(elem)
        result = new_k

        print("After cleaning")
        for element in result:
            print(element["cliente_afijo"])

        return  result

    # Update Data

    def update_app_data_afijos(self, cant_afijos, fecha_ultimo_afijo):
        table = "app_data"
        app_code = "app_pedigree"
        self.cursor.execute(f"SELECT * FROM app_data")
        response = self.cursor.fetchall()

        data_cliente_l = [(cant_afijos,
                           fecha_ultimo_afijo,
                           app_code)]

        if len(response) == 0:
            # data doesnt exist, create
            table_data = self.cursor.execute(f"SELECT * FROM {table}")
            columns = [description[0] for description in table_data.description]  # Lists the columns of the table
            sql_statement = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({', '.join(['?'] * len(columns))})"
            self.cursor.executemany(sql_statement, data_cliente_l)
            self.conn.commit()
        else:
            # Update
            self.cursor.execute(f'UPDATE app_data SET cant_afijos_hoy=?, fecha_ultimo_afijo=? WHERE app_id=?',
                                (cant_afijos, fecha_ultimo_afijo, app_code))
            self.conn.commit()

    def update_pedigree_data(self, edited_data: PedigreeData, edit_gene_data):

        nombre_cachorro = edited_data.nombre_cachorro
        sexo = edited_data.sexo
        color = edited_data.color
        nacimiento = edited_data.nacimiento
        raza = edited_data.raza
        criador = edited_data.criador
        afijo_madre = edited_data.afijo_madre
        afijo_padre = edited_data.afijo_padre
        nombre_madre = edited_data.nombre_madre
        nombre_padre = edited_data.nombre_padre
        propietario = edited_data.propietario
        homologacion = edited_data.homologacion

        certificado_code = float(edited_data.certificado_code)

        self.cursor.execute(f'UPDATE pedigrees SET nombre_cachorro=?, sexo=?,'
                            f' color=?, nacimiento=?, raza=?, criador=?, afijo_madre=?,'
                            f' afijo_padre=?, nombre_madre=?, nombre_padre=?,'
                            f' propietario=?, homologacion=?, genealogia_data=?'
                            f' WHERE certificado_code=?',
                            (nombre_cachorro, sexo,
                             color, nacimiento, raza, criador, afijo_madre,
                             afijo_padre, nombre_madre, nombre_padre,
                             propietario, homologacion, edit_gene_data, certificado_code))
        self.conn.commit()

    # Delete Data

    def delete_data(self, table, key_to_delete, value_for_key):
        try:
            t = (value_for_key,)
            self.cursor.execute(f"DELETE FROM {table} WHERE {key_to_delete}=?", t)
            self.conn.commit()
            return True
        except Exception:
            return False







