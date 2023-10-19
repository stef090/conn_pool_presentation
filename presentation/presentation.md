class: center, middle
background-image: url(https://th.bing.com/th/id/OIG.PdgarAuz7s12fBAtlQWV?pid=ImgGn)
# Database Connection Pooling

---

# Agenda

1. Introduction
2. Technicals
3. Postgres Architecture
4. What even is a connection?
5. Why multiprocessing?
6. The problem?
7. The solution...
8. ... with problems
9. Practical examples
10. Conclusion
11. Discussion
12. Resources
---

# Introduction

---

# Technicals
- Postgres Architecture
- Connection handling
- Connection pool techniques
- PgBouncer


???
We will be using Postgres for this presentation as most of us are familiar with it.

But, do we know how it all works under the hood?
Postgres and PgBouncer/PgPool.

Let's start with an overview of the Postgres architecture.

---

# Postgres Architecture
![Postgres Architecture](./graphics/postgres_architecture.png)

???
The **postgres server process** is the parent of all processes related to database cluster management.

Each **postgres backend process** handles all queries and statements issued by a connected client. Each backend process also allocates a local memory area for query processing. A backend process can only access one database at a time

All processes have access to a **shared memory** pool. All of the processes used by a PostgreSQL server use this shared memory to communicate with each other. 

There are also background processes which use the shared memory, each with their own specific task:

1. The **Background Writer** is responsible for reducing the I/O load on the system by moving dirty pages (pages that have been modified and not yet written to the disk) from the shared buffer cache to the disk
2. The **Checkpointer process** is responsible for issuing a checkpoint, which involves writing all dirty data pages from the shared buffer cache to the disk. 
3. The **Autovacuum** cleans and maintains the whole system by removing dead rows(tuples).
4. The **WAL**(Write Ahead Logger) is used to record transactional information before any transactional changes are applied to the database.
5. The **statistics collector** is used to for gathering and storing statistics on the activity of the database system.
6. The **archiver** process is responsible for managing the archiving of the WAL files.

# What even is a connection?
- TCP/IP connection
- Postgres server process takes connection request
- Process is forked to a new backend process
- 1 connection = 1 process
- Backend handles SQL queries, retrieving rows, returning results
- Terminated when a client disconnects

???
In the case of PostgreSQL, each new connection spawns a new process.
1 connection = 1 process. This was done as a safeguard to prevent database crashes and race conditions.

As well as this, applications are dependent on the OS threading libraries which can lead to all sorts of unstable behavior.

In the past, especially for Linux, forking a process was very expensive. Over the years and with optimizations, this has gone down considerably.

If a client wants to establish a connection, it must first contact the supervisor process at the port set for the Postgres server, typically port `5432`. The connection itself is a TCP/IP connection.

After a connection request is received, the `supervisor` will fork a new `backend` process.
The client will then start communicating with the backend process, which accepts and parses queries, creates *execution plans*, executes them, and returns the retrieved rows from the database by transmitting them over.


---

# Why multiprocessing?
- PRO:
	- Stability
	- Robustness
	- Security
	- Isolation
- CON:
	- Startup costs
	- Memory usage
	- OS limitations


???
While multiprocessing has several benefits, such as ensuring stability, robustness, and isolation when executing queries, there are of course drawbacks. 
The main drawback is the higher cost of process startup when compared to starting a thread. 
Each new process requires a certain amount of memory for its execution, including memory for various data structures, query execution, and caching.


---

# The problem?
 - Lots of connections and small transactions
 - Connections are dropped and restarted
 - Load is greater with each application(client) accessing the database
 
???
In modern web apps, clients tend to open a lot of connections, while transactions are kept very short.
Applications and developers are encouraged to drop connections, rather than hold on to them. 
This causes a lot of connections to start and drop very quickly, especially when more apps are accessing the same database backend.
 
---


# Connection Pool Architecture

![Connection Pool Architecture](./graphics/connection-pool-architecture.png)


---

# The solution?
 - Connection pooling
 - Most libraries implement it, SQLAlchemy included
 - Ensures connections are reused

???
There are many database access libraries which implement pooling, but they may wary in their behavior and implementation, which may then lead to strange behavior.
Factors to consider include **thread safety**, **connection validation**, **idle connection management**, and **efficient resource utilization**.
This has led to the creation of middlewares such as PGBouncer.

---

# ... with problems
  - different libs, different approaches
  - no guarantees of efficiency

---

# Practical examples
- 
---

# Conclusion

---

# Discussion

---

# Resources
https://scalegrid.io/blog/postgresql-connection-pooling-part-1-pros-and-cons/
https://scalegrid.io/blog/postgresql-connection-pooling-part-2-pgbouncer/
https://scalegrid.io/blog/postgresql-connection-pooling-part-3-pgpool-ii/
https://scalegrid.io/blog/postgresql-connection-pooling-part-4-pgbouncer-vs-pgpool/
