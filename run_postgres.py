import psycopg2
import time

# Wait for server to start
print("Waiting for server to start...")
time.sleep(5)

conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="your_new_user",
    password="qwerty",
    port="5432"
)

print("Server is running on port:", conn.get_dsn_parameters()['port'])

# Keep the program running
while True:
    try:
        time.sleep(1)
    except KeyboardInterrupt:
        break
