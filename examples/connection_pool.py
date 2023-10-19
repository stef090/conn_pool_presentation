import psycopg2
from queue import Queue
from threading import Lock

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
connection_pool = ConnectionPool(max_connections=5, database="your_db", user="your_user", password="your_password", host="your_host")

# Get a connection from the pool
conn = connection_pool.get_connection()

# Use the connection for database operations
cur = conn.cursor()
cur.execute("SELECT * FROM your_table")
rows = cur.fetchall()
print(rows)

# Release the connection back to the pool
connection_pool.release_connection(conn)

# Close all connections when done
connection_pool.close_all_connections()
