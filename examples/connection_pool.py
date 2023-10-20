from random import Random
from time import sleep

import psycopg2
from queue import Queue
from threading import Lock, Thread


class ConnectionPool:
    def __init__(self, max_connections, **kwargs):
        self.max_connections = max_connections
        self._connection_params = kwargs
        self._pool = Queue(max_connections)
        self._lock = Lock()

        for _ in range(max_connections):
            self._pool.put(self._create_connection())

    def _create_connection(self):
        return psycopg2.connect(**self._connection_params)

    def get_connection(self):
        with self._lock:
            if self._pool.empty():
                return None
            return self._pool.get()

    def release_connection(self, connection):
        if connection:
            self._pool.put(connection)

    def close_all_connections(self):
        with self._lock:
            while not self._pool.empty():
                connection = self._pool.get()
                connection.close()


# Example usage:
# Initialize the pool
connection_pool = ConnectionPool(
    max_connections=2,
    database="db",
    user="user",
    password="pass",
    host="localhost",
)


def simulate_client(client_id):

    while True:
        try:
            conn = connection_pool.get_connection()
            if conn is None:
                print(f"Client {client_id} could not acquire connection.")
                break
            cursor = conn.cursor()
            rand = Random()
            company_id = rand.randrange(1, 100)
            cursor.execute(
                f"SELECT * FROM machine_locations where owner_id={company_id};"
            )
            result = cursor.fetchall()
            print(f"Client {client_id} fetched data: {result}")
            connection_pool.release_connection(conn)
            print(f"Client {client_id} released connection.")
        except (Exception, psycopg2.Error) as error:
            print(f"Error occurred for client {client_id}: {error}")
            if conn:
                connection_pool.release_connection(conn)


def simulate_clients():
    for client_id in range(10):
        thread = Thread(target=simulate_client, args=(client_id,))
        thread.start()
        sleep(1)


if __name__ == "__main__":
    simulate_clients()
