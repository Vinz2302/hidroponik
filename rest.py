import psycopg2
from connect import connection
from config import load_config

def fetch_data():
    try:
        config = load_config()
        conn = connection(config)
        cursor = conn.cursor()
        query = "select * from users"

        cursor.execute(query)
        rows = cursor.fetchall()

        print("print each row and column")
        for row in rows:
            print("publisher_id = ", row[0], )
            print("publisher_name = ", row[1])
            print("publisher_email = ", row[2])
    except (Exception, psycopg2.Error) as error:
        print("Error while fetching data from postgresql", error)

    finally:
        if conn:
            cursor.close()
            conn.close()
            print("server closed")

if __name__ == "__main__":
    fetch_data() #call function when running the scripts