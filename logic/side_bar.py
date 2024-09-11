# side_bar.py

import streamlit as st
from streamlit_option_menu import option_menu
from logic.tracebacks import *
import pandas as pd
import io
# import psycopg2
# import pytds
# import pymysql

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
                options=['Load File', 'SQL Login', 'PostgreSQL Login', 'Microsoft SQL Login'],
                icons=['load', 'sql', 'PostgreSQL Login', 'sqlserver'],
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

    def connector(self, username, password, host, port, db_type, database=None, tables=None):
        username = username.lower()
        password = password
        host = host.lower()

        try:
            port = int(port)
            if port < 0 or port > 65535:
                raise ValueError("Invalid port. Please enter a valid port number between 0 and 65535.")
        except ValueError as e:
            error_message = "Invalid or empty inputs, please ensure all inputs are properly filled."
            print(error_message)
            self.st.error(error_message)
            return None

        if db_type == 'mysql':
            try:
                import pymysql
                cnx = pymysql.connect(
                    user=username,
                    password=password,
                    host=host,
                    port=port
                )
                print(f"Connected to MySQL Server: {cnx.get_server_info()}")
                return cnx

            except (pymysql.Error, ValueError, TypeError, AttributeError) as err:
                error_message = sql_error(err)
                print(error_message)
                self.st.error(error_message)
                return None

        elif db_type == 'postgresql':
            try:
                import psycopg2
                cnx = psycopg2.connect(
                    user=username,
                    password=password,
                    host=host,
                    port=port
                )
                print(f"Connected to PostgreSQL Server: {cnx.server_version}")
                return cnx

            except (psycopg2.Error, ValueError, TypeError, AttributeError) as err:
                error_message = psql_error(err)
                print(error_message)
                self.st.error(error_message)
                return None

        elif db_type == 'mssql':
            try:
                import pytds
                cnx = pytds.connect(
                    user=username,
                    password=password,
                    host=host,
                    port=port,
                    database='master'
                )
                print(f"Connected to MSSQL Server: {cnx.version}")
                return cnx

            except (pytds.Error, ValueError, TypeError, AttributeError) as err:
                error_message = mssql_error(err)
                print(error_message)
                self.st.error(error_message)
                return None

        else:
            error_message = "Invalid db_type. Please enter 'mysql', 'postgresql' or 'mssql'."
            print(error_message)
            self.st.error(error_message)
            return None


    def process_data(self, cnx, db_type):
        try:
            if db_type == 'mysql' or db_type == 'postgresql' or db_type == 'mssql':
                cursor = cnx.cursor()
                cursor.execute("SHOW DATABASES" if db_type == 'mysql' else "SELECT datname FROM pg_database" if db_type == 'postgresql' else 'SELECT name FROM sys.databases;')
                databases = [db[0] for db in cursor.fetchall()]
                selected_db = self.st.selectbox('Select Database', databases)

                if selected_db:
                    if db_type == 'mysql' or db_type == 'postgresql':
                        cursor.execute(f"USE {selected_db}" if db_type == 'mysql' else f"SET search_path TO {selected_db};")
                    else:
                        cursor.execute(f"USE {selected_db};")
                    cursor.execute("SHOW TABLES" if db_type == 'mysql' else "SELECT table_name FROM information_schema.tables" if db_type == 'postgresql' else 'SELECT name FROM sys.tables')
                    available_tables = [table[0] for table in cursor.fetchall()]
                    selected_tables = self.st.multiselect('Select Table(s)', available_tables)

                    if selected_tables:
                        login = self.st.button('Login')

                        if login:
                            dfs = []
                            for table in selected_tables:
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
        except Exception as e:
            self.st.error(e)


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
                sql_data = self.connector(username, password, host, port, 'mysql')
                if sql_data is not None:
                    return self.process_data(sql_data, 'mysql')

            if selected == 'PostgreSQL Login':
                username = self.st.text_input('Username')
                password = self.st.text_input('Password', type='password')
                host = self.st.text_input('Host')
                port = self.st.text_input('Port')
                psql_data = self.connector(username, password, host, port, 'postgresql')
                if psql_data is not None:
                    return self.process_data(psql_data, 'postgresql')

            if selected == 'Microsoft SQL Login':
                username = self.st.text_input('Username')
                password = self.st.text_input('Password', type='password')
                host = self.st.text_input('Host')
                port = self.st.text_input('Port')
                msql_data = self.connector(username, password, host, port, 'mssql')
                if msql_data is not None:
                    return self.process_data(msql_data, 'mssql')