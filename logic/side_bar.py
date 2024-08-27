# side_bar.py

import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import io
import psycopg2
import pytds
import deta
import pymongo
import pymysql
import urllib.parse

class Side:
    def __init__(self):
        self.st = st
        self.file_uploader_key = None

    def donate(self):
        for _ in range(2):
            st.write('#')
        url = "https://revolut.me/cosminhbs7"
        button_code = f"""
                <style>
                .custom-button {{
                    display: inline-block;
                    padding: 10px 20px;
                    font-size: 16px;
                    font-weight: bold;
                    color: white;
                    background-color: #262730;
                    border: none;
                    border-radius: 5px;
                    text-align: center;
                    text-decoration: none;
                    width: 100%;
                    transition: background-color 0.3s ease;
                }}
                .custom-button:hover {{
                    background-color: #6a2336;
                    color: white;
                }}
                </style>
                <a href="{url}" target="_blank" class="custom-button">Buy Me A Coffee</a>
                """
        self.st.markdown(button_code, unsafe_allow_html=True)

    def info_btn(self, key):
        if 'info_shown' not in st.session_state:
            st.session_state.info_shown = False

        pg_btn = self.st.button('READ', key=key)

        if pg_btn:
            st.session_state.info_shown = not st.session_state.info_shown

        if st.session_state.info_shown:
            self.st.info(
                """
                You can add one table or multiple tables separated by commas.
                 * Single: table1
                 * Multiple: table1, table2

                When you load multiple tables, their data is combined into one big dataset. However, the tables are not matched up based on a common column.

                For example, let's say you have two tables:
                 * Table 1 has columns for city and name.
                 * Table 2 has columns for age and ID.

                If you try to use the city from Table 1 and the ID from Table 2 together, you'll get empty or null data. This is because the tables are not connected in a way that allows you to use columns from both tables together.
                """
            )

    def header(self):
        st.set_page_config(layout="wide")
        self.st.title('DataPulse')
        self.st.markdown('<p style="font-size: small;">© 2024 Developed by CosminT. All rights reserved.</p>', unsafe_allow_html=True)

    def footer(self):
        pass

    def container(self):
        with self.st.container():
            selected = option_menu(
                menu_title=None,
                options=['Load File', 'SQL Login', 'PostgreSQL Login', 'Microsoft SQL Login', 'DETA Login', 'MongoDB Login'],
                icons=['load', 'sql', 'PostgreSQL Login', 'sqlserver', 'deta', 'mongodb'],
                default_index=0,
                orientation="vertical",
            )
        return selected

    def file(self):
        uploaded_file = self.st.file_uploader('Upload Your Excel File', type=['csv', 'xlsx', 'xls'])

        if uploaded_file is not None:
            if uploaded_file.type in ['text/csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
                self.st.success(f'File "{uploaded_file.name}" uploaded successfully!')

                try:
                    # If CSV file
                    if uploaded_file.type == 'text/csv':
                        content = uploaded_file.getvalue().decode('utf-8', errors='replace')
                        df = pd.read_csv(io.StringIO(content), delimiter=',', engine='python')

                    # If Excel file
                    else:
                        df = pd.read_excel(uploaded_file)

                    return df

                except Exception as e:
                    self.st.error(f"An error occurred while processing the file: {e}")

            else:
                self.st.error(f'File "{uploaded_file.name}" is not supported!')

        return None

    # SQL DB
    #TODO SQL Login
    def sql_connector(self, username, password, host, port, database, tables):
        username = username.lower()
        password = password
        host = host.lower()
        try:
            port = int(port)
            if port < 0 or port > 65535:
                raise ValueError("Invalid port. Please enter a valid port number between 0 and 65535.")
        except ValueError as e:
            error_message = f"Invalid or empty inputs, please ensure all imputs are properly filled."
            print(error_message)
            self.st.error(error_message)
            return None
        database = database
        tables = tables

        print(f"username: {username}")
        print(f"password: {password}")
        print(f"host: {host}")
        print(f"port: {port}")
        print(f"database: {database}")

        try:
            cnx = pymysql.connect(
                user=username,
                password=password,
                host=host,
                port=port,
                database=database
            )
            print(f"Connected to MySQL Server: {cnx.get_server_info()}")
            cursor = cnx.cursor()

            dfs = []
            for table in tables:
                print(f"Executing SQL query: SELECT * FROM {table}")
                cursor.execute(f"SELECT * FROM {table}")
                results = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]
                df = pd.DataFrame(results, columns=columns)
                df = df.reset_index(drop=True)
                dfs.append(df)

            concatenated_df = pd.concat(dfs, ignore_index=True)
            concatenated_df.to_csv('sql_output.csv', index=False)
            return concatenated_df

        except (pymysql.Error, ValueError, TypeError, AttributeError) as err:
            error_message = f"Error occurred: {err}"

            if isinstance(err, ValueError):
                if 'invalid literal' in str(err):
                    error_message += "\nInvalid input type. Please ensure that port is an integer."
                else:
                    error_message += "\nInvalid input. Please verify the provided inputs."

            elif isinstance(err, TypeError):
                error_message += "\nInvalid argument type. Please check the types of provided inputs."

            elif isinstance(err, AttributeError):
                error_message += "\nMissing or undefined attribute. Please verify the inputs and code structure."

            elif isinstance(err, pymysql.Error):
                if err.args[0] == 1045:
                    error_message += "\nInvalid username or password. Please check your credentials."
                elif err.args[0] == 1049:
                    error_message += "\nDatabase does not exist. Please check the database name."
                elif err.args[0] == 1146:
                    error_message += f"\nTable '{tables[0]}' does not exist. Please check if the table names are correct and exist in the database."
                elif err.args[0] == 1064:
                    if not database:
                        error_message = "\nDatabase name is missing. Please provide a valid database name."
                    elif not tables:
                        error_message = "\nTable name is missing. Please provide a valid table name."
                    else:
                        error_message = "\nSQL syntax error. Please check if you are missing or providing incorrect table names."
                elif err.args[0] == 2003:
                    error_message += "\nConnection refused. Please check the host and port."
                elif err.args[0] == 2005:
                    error_message += "\nUnknown host. Please check the host."
                elif err.args[0] == 2006:
                    error_message += "\nMySQL server has gone away. Please check the connection."
                else:
                    error_message += f"\nUnexpected error. Error code: {err.args[0]}"

            else:
                error_message += "\nUnexpected error. Please check the inputs and code structure."

            error_message += "\n\nTroubleshooting steps:"
            error_message += "\n1. Verify your connection details (username, password, host, port, database)."
            error_message += "\n2. Ensure the database exists and you have the necessary permissions."
            error_message += "\n3. Check if the specified tables exist in the database."
            error_message += "\n4. If you provided a list of tables, make sure it's not empty."
            error_message += "\n5. Double-check for any typos in table names."

            if not username:
                error_message += "\nPlease provide a valid username."
            if not password:
                error_message += "\nPlease provide a valid password."
            if not host:
                error_message += "\nPlease provide a valid host."
            if not port:
                error_message += "\nPlease provide a valid port."
            if not database:
                error_message += "\nPlease provide a valid database."
            if not tables:
                error_message += "\nPlease provide a valid list of tables."

            print(error_message)
            self.st.error(error_message)
            return None

    #TODO PostgreSQL Login
    def pgsql_connector(self, username, password, host, port, database, tables):
        username = username.lower()
        password = password
        host = host.lower()
        try:
            port = int(port)
            if port < 0 or port > 65535:
                raise ValueError("Invalid port. Please enter a valid port number between 0 and 65535.")
        except ValueError as e:
            error_message = f"Invalid or empty inputs, please ensure all imputs are properly filled."
            print(error_message)
            self.st.error(error_message)
            return None
        database = database
        tables = tables

        print(f"username: {username}")
        print(f"password: {password}")
        print(f"host: {host}")
        print(f"port: {port}")
        print(f"database: {database}")

        try:
            conn = psycopg2.connect(
                dbname=database,
                user=username,
                password=password,
                host=host,
                port=port
            )
            print(f"Connected to PostgreSQL Server: {conn.server_version}")
            cur = conn.cursor()

            dfs = []
            for table in tables:
                print(f"Executing SQL query: SELECT * FROM {table}")
                cur.execute(f"SELECT * FROM {table}")
                results = cur.fetchall()
                columns = [desc[0] for desc in cur.description]
                df = pd.DataFrame(results, columns=columns)
                df = df.reset_index(drop=True)
                dfs.append(df)

            concatenated_df = pd.concat(dfs, ignore_index=True)
            concatenated_df.to_csv('pgsql_output.csv', index=False)
            return concatenated_df

        except (psycopg2.Error, ValueError, TypeError, AttributeError) as err:
            error_message = f"Error occurred: {err}"

            if isinstance(err, ValueError):
                if 'invalid literal' in str(err):
                    error_message += "\nInvalid input type. Please ensure that port is an integer."
                else:
                    error_message += "\nInvalid input. Please verify the provided inputs."

            elif isinstance(err, TypeError):
                error_message += "\nInvalid argument type. Please check the types of provided inputs."

            elif isinstance(err, AttributeError):
                error_message += "\nMissing or undefined attribute. Please verify the inputs and code structure."

            elif isinstance(err, psycopg2.Error):
                if not database:
                    error_message = "\nDatabase name is missing. Please provide a valid database name."
                elif err.pgcode == '28000':
                    error_message += "\nInvalid username or password. Please check your credentials."
                elif err.pgcode == '3D000':
                    error_message += "\nDatabase does not exist. Please check the database name."
                elif err.pgcode == '42P01':
                    error_message += f"\nTable '{tables[0]}' does not exist. Please check if the table names are correct and exist in the database."
                elif err.pgcode == '42601':
                    if not tables:
                        error_message = "\nTable name is missing. Please provide a valid table name."
                    else:
                        error_message = "\nSQL syntax error. Please check if you are missing or providing incorrect table names."
                elif err.pgcode == '08006':
                    error_message += "\nConnection refused. Please check the host and port."
                elif err.pgcode == '08001':
                    error_message += "\nUnknown host. Please check the host."
                elif err.pgcode == '57P01':
                    error_message += "\nPostgreSQL server has gone away. Please check the connection."
                else:
                    error_message += f"\nUnexpected error. Error code: {err.pgcode}"

            else:
                error_message += "\nUnexpected error. Please check the inputs and code structure."

            error_message += "\n\nTroubleshooting steps:"
            error_message += "\n1. Verify your connection details (username, password, host, port, database)."
            error_message += "\n2. Ensure the database exists and you have the necessary permissions."
            error_message += "\n3. Check if the specified tables exist in the database."
            error_message += "\n4. If you provided a list of tables, make sure it's not empty."
            error_message += "\n5. Double-check for any typos in table names."

            if not username:
                error_message += "\nPlease provide a valid username."
            if not password:
                error_message += "\nPlease provide a valid password."
            if not host:
                error_message += "\nPlease provide a valid host."
            if not port:
                error_message += "\nPlease provide a valid port."
            if not database:
                error_message += "\nPlease provide a valid database."
            if not tables:
                error_message += "\nPlease provide a valid list of tables."

            print(error_message)
            self.st.error(error_message)
            return None

    #TODO Microsoft SQL Server Login
    def mssql_connector(self, username, password, host, port, database, tables):
        username = username.lower()
        password = password
        host = host.lower()
        try:
            port = int(port)
            if port < 0 or port > 65535:
                raise ValueError("Invalid port. Please enter a valid port number between 0 and 65535.")
        except ValueError as e:
            error_message = f"Invalid or empty inputs, please ensure all imputs are properly filled."
            print(error_message)
            self.st.error(error_message)
            return None
        database = database
        tables = tables

        print(f"username: {username}")
        print(f"password: {password}")
        print(f"host: {host}")
        print(f"port: {port}")
        print(f"database: {database}")

        try:
            print(f"Connecting to Microsoft SQL Server at {host}:{port}, database: {database}")
            conn = pytds.connect(
                dsn=host,
                database=database,
                user=username,
                password=password,
                port=port
            )
            print("Connected to Microsoft SQL Server")

            dfs = []
            for table in tables:
                print(f"Executing SQL query: SELECT * FROM {table}")
                cursor = conn.cursor()
                cursor.execute(f"SELECT * FROM {table}")
                columns = [column[0] for column in cursor.description]
                rows = cursor.fetchall()
                df = pd.DataFrame(rows, columns=columns)
                dfs.append(df)

            concatenated_df = pd.concat(dfs, ignore_index=True)
            concatenated_df.to_csv('mssql_output.csv', index=False)
            return concatenated_df

        except (pytds.Error, ValueError, TypeError, AttributeError) as err:
            error_message = f"Error occurred: {err}"

            if isinstance(err, ValueError):
                if 'invalid literal' in str(err):
                    error_message += "\nInvalid input type. Please ensure that port is an integer."
                else:
                    error_message += "\nInvalid input. Please verify the provided inputs."

            elif isinstance(err, TypeError):
                error_message += "\nInvalid argument type. Please check the types of provided inputs."

            elif isinstance(err, AttributeError):
                error_message += "\nMissing or undefined attribute. Please verify the inputs and code structure."

            elif isinstance(err, pytds.Error):
                error_str = str(err)
                if "Cannot open database" in error_str:
                    error_message += "\nDatabase not found or access denied. Please check the database name."
                elif "The login failed" in error_str or "Login failed for user" in error_str:
                    error_message += "\nInvalid username or password. Please check your credentials."
                elif "Failed to establish a connection" in error_str or "Connection refused" in error_str:
                    error_message += "\nFailed to establish connection to the server. Please check the host and port."
                elif "Invalid object name" in error_str:
                    error_message += "\nTable name is incorrect. Please check the table name."
                elif "Incorrect syntax near 'FROM'" in error_str:
                    error_message += "\nNo table name provided. Please check the table name."
                elif "database name is empty" in error_str.lower() or 'select * from ' in error_str.lower() or "from " in error_str.lower() or ' table not exist ' in error_str.lower() or " Invalid column name " in error_str or 'Error invalid number ' in error_str or " Select value don not correct datatype ' is different":
                    error_message += "\nIncorrect syntax in the SQL statement or Data corruption exists .Please re-evaluate input value check server sql driver."
                elif "database" in error_str.lower():
                    error_message += "\nDatabase does not exist. Please check the database name."

            else:
                error_message += "\nUnexpected error. Please check the inputs and code structure."

            error_message += "\n\nTroubleshooting steps:"
            error_message += "\n1. Verify your connection details (username, password, host, port, database)."
            error_message += "\n2. Ensure the database exists and you have the necessary permissions."
            error_message += "\n3. Check if the specified tables exist in the database."
            error_message += "\n4. If you provided a list of tables, make sure it's not empty."
            error_message += "\n5. Double-check for any typos in table names."

            if not username:
                error_message += "\nPlease provide a valid username."
            if not password:
                error_message += "\nPlease provide a valid password."
            if not host:
                error_message += "\nPlease provide a valid host."
            if not database:
                error_message += "\nPlease provide a valid database."
            if not tables:
                error_message += "\nPlease provide a valid list of tables."

            print(error_message)
            self.st.error(error_message)
            return None

    #TODO DETA Login Login
    def deta_connector(self, deta_key, database, tables):
        deta_key = deta_key
        database = database
        tables = tables

        print(f"Project Key: {deta_key}")
        print(f"Database Name: {database}")
        print(f"Tables: {tables}")

        try:
            deta_client = deta.Deta(deta_key)
            db = deta_client.Base(database)

            # Check if the database is empty
            if not db.fetch().items:
                error_message = "Database is empty or does not exist. Please check the database name."
                print(error_message)
                self.st.error(error_message)
                return None

            dfs = []
            for table in tables:
                print(f"Executing Deta query: get all items from {table}")
                items = db.fetch().items
                df = pd.DataFrame(items)
                dfs.append(df)

            concatenated_df = pd.concat(dfs, ignore_index=True)
            concatenated_df.to_csv('deta_output.csv', index=False)
            return concatenated_df

        except (Exception) as err:
            error_message = f"Error occurred: {err}"

            if 'Unauthorized' in str(err):
                error_message += "\nInvalid Deta Key. Please check your credentials."
            elif len(deta_key) == 0:
                error_message += "\nDeta Key is missing."
            elif len(database) == 0:
                error_message += "\nDatabase is empty."
            elif len(tables) == 1 and tables[0] == '':
                error_message += "\nTable is empty."

            error_message += "\n\nTroubleshooting steps:"
            error_message += "\n1. Verify your Deta Key."
            error_message += "\n2. Ensure the database exists and you have the necessary permissions."
            error_message += "\n3. Check if the specified tables exist in the database."
            error_message += "\n4. If you provided a list of tables, make sure it's not empty."
            error_message += "\n5. Double-check for any typos in table names."

            if not deta_key:
                error_message += "\nPlease provide a valid Deta Key."
            if not database:
                error_message += "\nPlease provide a valid database."
            if not tables:
                error_message += "\nPlease provide a valid list of tables."

            print(error_message)
            self.st.error(error_message)
            return None

    # No SQL DB
    #TODO MongoDB Login
    def mongodb_connector(self, username, password, host, port, database, collection):
        username = urllib.parse.quote_plus(username.lower())
        password = urllib.parse.quote_plus(password)
        host = host.lower()
        try:
            port = int(port)
            if port < 0 or port > 65535:
                raise ValueError("Invalid port. Please enter a valid port number between 0 and 65535.")
        except ValueError as e:
            error_message = f"Invalid or empty inputs, please ensure all imputs are properly filled."
            print(error_message)
            self.st.error(error_message)
            return None
        database = database
        collection = collection

        print(f"username: {username}")
        print(f"password: {password}")
        print(f"host: {host}")
        print(f"port: {port}")
        print(f"database: {database}")
        print(f"collection: {collection}")

        try:
            client = pymongo.MongoClient(f"mongodb://{username}:{password}@{host}:{port}/admin")
            print(f"Connected to MongoDB Server: {client.server_info()['version']}")

            if database not in client.list_database_names():
                raise pymongo.errors.OperationFailure("Database does not exist. Please check the database name.")

            db = client[database]
            if collection not in db.list_collection_names():
                raise pymongo.errors.CollectionInvalid("Collection does not exist. Please check the collection name.")

            coll = db[collection]

            cursor = coll.find()
            data = list(cursor)
            df = pd.DataFrame(list(data))
            df = df.reset_index(drop=True)
            df.to_csv('mongodb_output.csv', index=False)
            return df

        except (pymongo.errors.PyMongoError, ValueError, TypeError, AttributeError) as err:
            error_message = f"Error occurred: "

            if isinstance(err, pymongo.errors.OperationFailure):
                if 'nonexistent database' in str(err).lower():
                    error_message += "\nDatabase does not exist. Please check the database name."
                elif 'nonexistent collection' in str(err).lower():
                    error_message += "\nCollection does not exist. Please check the collection name."
                else:
                    error_message += "\nOperation failed. Please verify the database and collection names."
            elif isinstance(err, pymongo.errors.InvalidName):
                error_message += "\nInvalid database or collection name. Please ensure they are correct."
            elif isinstance(err, pymongo.errors.CollectionInvalid):
                error_message += "\nCollection does not exist. Please check the collection name."
            elif isinstance(err, ValueError):
                error_message += "\nInvalid input. Please verify the provided inputs."
            elif isinstance(err, TypeError):
                error_message += "\nInvalid argument type. Please check the types of provided inputs."
            elif isinstance(err, AttributeError):
                error_message += "\nMissing or undefined attribute. Please verify the inputs and code structure."
            else:
                error_message += "\nUnexpected error. Please check the inputs and code structure."

            error_message += "\n\nTroubleshooting steps:"
            error_message += "\n1. Verify your connection details (username, password, host, port, database)."
            error_message += "\n2. Ensure the database exists and you have the necessary permissions."
            error_message += "\n3. Check if the specified collection exists in the database."
            error_message += "\n4. Double-check for any typos in collection names."

            print(error_message)
            self.st.error(error_message)
            return None

    # SideBar Connection
    def side(self):
        with self.st.sidebar:
            selected = self.container()
            if selected == 'Load File':
                data = self.file()
                if data is not None and not data.empty:
                    self.donate()
                    return data
                elif data is None:
                    # self.donate()
                    self.st.error('No file uploaded!')
                self.donate()


            if selected == 'SQL Login':
                username = self.st.text_input('Username')
                password = self.st.text_input('Password', type='password')
                host = self.st.text_input('Host')
                port = self.st.text_input('Port')
                database = self.st.text_input('Database')
                self.info_btn('1')
                tables = self.st.text_input('Tables (comma-separated or single)').split(',')
                login = self.st.button('Login')
                if login:
                    sql_data = self.sql_connector(username, password, host, port, database, tables)
                    if sql_data is not None:
                        self.donate()
                        return sql_data
                self.donate()

            if selected == 'PostgreSQL Login':
                username = self.st.text_input('Username')
                password = self.st.text_input('Password', type='password')
                host = self.st.text_input('Host')
                port = self.st.text_input('Port')
                database = self.st.text_input('Database')
                self.info_btn('2')
                tables = self.st.text_input('Tables (comma-separated or single)').split(',')
                login = self.st.button('Login')
                if login:
                    pgsql_data = self.pgsql_connector(username, password, host, port, database, tables)
                    if pgsql_data is not None:
                        self.donate()
                        return pgsql_data
                self.donate()

            if selected == 'Microsoft SQL Login':
                username = self.st.text_input('Username')
                password = self.st.text_input('Password', type='password')
                host = self.st.text_input('Host')
                port = self.st.text_input('Port')
                database = self.st.text_input('Database')
                self.info_btn('3')
                tables = self.st.text_input('Tables (comma-separated or single)').split(',')
                login = self.st.button('Login')
                if login:
                    mssql_data = self.mssql_connector(username, password, host, port, database, tables)
                    if mssql_data is not None:
                        self.donate()
                        return mssql_data
                self.donate()

            if selected == 'DETA Login':
                deta_key = self.st.text_input('Deta Key')
                database = self.st.text_input('Database Name')
                self.info_btn('4')
                tables = self.st.text_input('Tables (comma-separated or single)').split(',')
                login = self.st.button('Login')
                if login:
                    deta_data = self.deta_connector(deta_key, database, tables)
                    if deta_data is not None:
                        self.donate()
                        return deta_data
                self.donate()

            if selected == 'MongoDB Login':
                username = self.st.text_input('Username')
                password = self.st.text_input('Password', type='password')
                host = self.st.text_input('Host')
                port = self.st.text_input('Port')
                database = self.st.text_input('Database')
                self.info_btn('5')
                collection = self.st.text_input('Collection')
                login = self.st.button('Login')
                if login:
                    mongodb_data = self.mongodb_connector(username, password, host, port, database, collection)
                    if mongodb_data is not None:
                        self.donate()
                        return mongodb_data
                self.donate()
