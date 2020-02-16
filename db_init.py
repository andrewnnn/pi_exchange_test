import sqlite3
import names
import time
from random import seed, choice
import string
                                    
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Sqlite Version: ", sqlite3.version)
    except:
        print("create connection erorr")
    
    return conn
 
def create_table(conn):
    sql = """ CREATE TABLE IF NOT EXISTS Customers (
                                    id integer PRIMARY KEY,
                                    name text NOT NULL,
                                    phone_number text
                                ); """
    try:
        c = conn.cursor()
        c.execute(sql)
    except:
        print("create table erorr")

def create_customer(conn, customer):
    sql = ''' INSERT INTO customers(name,phone_number)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, customer)
    return cur.lastrowid

def create_index(conn):
    sql = ''' CREATE INDEX idx_customers_phone_number
              ON customers (phone_number); '''
    try:
        c = conn.cursor()
        c.execute(sql)
    except:
        print("create index erorr")

if __name__ == '__main__':
    t = time.time()
    conn = create_connection("sqlite.db")

    # create customers table
    if conn is not None:
        create_table(conn)
    else:
        print("Error! cannot create the database connection.")

    # generate 10,000 random customer rows
    with conn:
        seed(0)
        cur = conn.cursor()
        # 10 batch inserts
        for _ in range(10):
            cur.execute('BEGIN TRANSACTION')
            # of 1000 inserts
            for _ in range(1000):
                phone_number = ''.join(choice(string.digits) for _ in range(11))
                customer = (names.get_full_name(), phone_number)
                create_customer(conn, customer)
            cur.execute('COMMIT')
        
        create_index(conn)

    print("\n Time Taken: {:.3f} sec".format(time.time()-t))

