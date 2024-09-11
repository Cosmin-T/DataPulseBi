"""
import deta
import pymongo
import urllib.parse

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
        return None """