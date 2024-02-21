import psycopg2
from config import load_config

def connection(config):
    """Connect to the Postgresql database server"""
    try:
        #connecting to the Postgresql server
        with psycopg2.connect(**config) as conn:
            print('Connected to the database')
            return conn
    except (psycopg2.DatabaseError, Exception) as error:
        print(error)

#test database connection
# if __name__ == '__main__' :
#     config = load_config()
#     connection(config)