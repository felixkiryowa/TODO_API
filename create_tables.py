import psycopg2
from config import config
 
 
def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE users (
            user_id SERIAL PRIMARY KEY,
            public_id VARCHAR(60) NOT NULL UNIQUE,
            name VARCHAR(60) NOT NULL UNIQUE,
            password VARCHAR(60) NOT NULL,
            admin BOOLEAN NOT NULL
        )
        """,
        """
        CREATE TABLE todo (
                id SERIAL PRIMARY KEY,
                text VARCHAR(60) NOT NULL,
                complete BOOLEAN NOT NULL,
                user_id INT REFERENCES users (user_id)
                    ON UPDATE CASCADE ON DELETE CASCADE
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table one by one
        for command in commands:
            cur.execute(command)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ ==  '__main__':
    create_tables()