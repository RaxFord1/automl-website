import psycopg2


def ping_db():
    try:
        # Connect to your postgres DB
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="postgres",
            host="db",
            port="5432"
        )
        # Open a cursor to perform database operations
        cur = conn.cursor()

        # Execute a command: this creates a new table
        cur.execute("SELECT 1")

        # Retrieve query results
        result = cur.fetchone()
        print("Ping successful, result:", result)

        # Close communication with the database
        cur.close()
        conn.close()

    except Exception as e:
        print("Error while pinging database:", e)


ping_db()
