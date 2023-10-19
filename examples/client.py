import psycopg2
from time import sleep
from threading import Thread

# Function to simulate client behavior without connection pooling
def simulate_client(client_id):
    conn = psycopg2.connect(
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port",
        database="your_database"
    )

    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM your_table;")
        result = cursor.fetchall()
        print(f"Client {client_id} fetched data: {result}")
    except (Exception, psycopg2.Error) as error:
        print(f"Error occurred for client {client_id}: {error}")
    finally:
        if conn:
            cursor.close()
            conn.close()

# Simulate multiple clients accessing the database
for i in range(5):
    thread = Thread(target=simulate_client, args=(i,))
    thread.start()
    sleep(1)  # Introduce a delay to stagger client connections
