import sqlite3

conn = sqlite3.connect('python_web.db')
cur = conn.cursor()


create_users_table = """
    CREATE TABLE users (
    user_id INTEGER PRIMARY KEY NOT NULL,
    username TEXT,
    password TEXT
);
"""

create_tasks_table = """
CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY NOT NULL,
    title TEXT,
    created_at DATETIME,
    is_completed BOOLEAN, 
    user_id INTEGER,
    FOREIGN KEY(user_id) REFERENCES users(user_id)  -- to define a relationship with the users table
);
"""

try:
    cur.execute(create_users_table)
    cur.execute(create_tasks_table)
    conn.commit()
    print("Tables created successfully")
except sqlite3.Error as error:
    print('Error while creating tables', error)
finally:
    cur.close()
    conn.close()
    
