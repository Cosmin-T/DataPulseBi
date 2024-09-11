def sql_error(err):
    import pymysql
    error_message = f"An error occurred: {err}"

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
            error_message += f"\nTable does not exist. Please check if the table names are correct and exist in the database."
        elif err.args[0] == 1064:
            error_message += "\nSQL syntax error. Please check if you are missing or providing incorrect table names."
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

    return error_message

def psql_error(err):
    import psycopg2
    error_message = f"An error occurred: {err}"

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
        if err.args[0] == 1045:
            error_message += "\nInvalid username or password. Please check your credentials."
        elif err.args[0] == 1049:
            error_message += "\nDatabase does not exist. Please check the database name."
        elif err.args[0] == 1146:
            error_message += f"\nTable does not exist. Please check if the table names are correct and exist in the database."
        elif err.args[0] == 1064:
            error_message += "\nSQL syntax error. Please check if you are missing or providing incorrect table names."
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

    return error_message

def mssql_error(err):
    import pytds
    error_message = f"An error occurred: {err}"

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
        if err.args[0] == 1045:
            error_message += "\nInvalid username or password. Please check your credentials."
        elif err.args[0] == 1049:
            error_message += "\nDatabase does not exist. Please check the database name."
        elif err.args[0] == 1146:
            error_message += f"\nTable does not exist. Please check if the table names are correct and exist in the database."
        elif err.args[0] == 1064:
            error_message += "\nSQL syntax error. Please check if you are missing or providing incorrect table names."
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

    return error_message
