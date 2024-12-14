import psycopg2

def connect_to_db():
    try:
        return psycopg2.connect(database="postgres",
                        host="localhost",
                        user="postgres",
                        password="postgrespswd",
                        port="5432")
    except psycopg2.OperationalError:
        raise Exception("Unable to connect to database")