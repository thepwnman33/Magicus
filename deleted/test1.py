import psycopg2

# Enter your database credentials here
DB_NAME = "postgres"
DB_USER = "your_new_user"
DB_PASSWORD = "qwerty"
DB_HOST = "localhost"
DB_PORT = "5432"

try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    print("Connected successfully!")

    # Close the connection60
    conn.close()

except psycopg2.Error as e:
    print("Error connecting to database:", e)
    