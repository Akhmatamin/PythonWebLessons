import psycopg2
from psycopg2 import sql

dbname = 'python_web'
user = 'postgres'
password = 'adminadmin'
host = 'localhost'
port = '5432'

create_users_table = """
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username TEXT,
    password TEXT
);
"""

create_tasks_table = """
    CREATE TABLE tasks (
        task_id      SERIAL PRIMARY KEY,
        title        TEXT,
        created_at   TIMESTAMP,
        is_completed BOOLEAN,
        user_id      INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (user_id) \
    );
"""

conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)
cur = conn.cursor()

try:
    cur.execute(create_users_table)
    cur.execute(create_tasks_table)
    conn.commit()
    print("Tables created successfully")
except Exception as e:
    print('Error while executing sql', e)
    conn.rollback()
finally:
    cur.close()
    conn.close()
