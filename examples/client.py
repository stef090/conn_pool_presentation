from random import Random

import psycopg2
from time import sleep
from threading import Thread


def simulate_client(client_id):
    conn = psycopg2.connect(
        user="your_host",
        password="your_pass",
        host="localhost",
        port="5432",
        database="your_host",
    )

    cursor = conn.cursor()
    rand = Random()
    while True:
        try:
            company_id = rand.randrange(1, 100)
            cursor.execute(
                f"SELECT * FROM machine_locations where owner_id={company_id};"
            )
            result = cursor.fetchall()
            print(f"Client {client_id} fetched data: {result}")
        except (Exception, psycopg2.Error) as error:
            print(f"Error occurred for client {client_id}: {error}")
            if conn:
                cursor.close()
                conn.close()


# Simulate multiple clients accessing the database
def simulate_clients():
    for client_id in range(10):
        thread = Thread(target=simulate_client, args=(client_id,))
        thread.start()
        sleep(1)


if __name__ == "__main__":
    simulate_clients()
