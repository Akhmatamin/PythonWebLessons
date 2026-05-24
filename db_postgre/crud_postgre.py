import psycopg2
from hashlib import sha1

from datetime import date

def insert_users(conn, users):
    with conn.cursor() as cur:
        insert_query = "INSERT INTO users (username, password) VALUES (%s, %s)"
        cur.executemany(insert_query, users)
        conn.commit()

def insert_tasks(conn, tasks):
    with conn.cursor() as cur:
        insert_query = "INSERT INTO tasks (title, created_at, is_completed, user_id) VALUES (%s, %s, %s, %s)"
        cur.executemany(insert_query, tasks)
        conn.commit()

def select_users_by_id(conn, user_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE user_id = %s", (user_id,))
        return cur.fetchall()

def select_users_by_username(conn, username):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        return cur.fetchall()

def select_tasks_by_id(conn, task_id):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tasks WHERE task_id = %s", (task_id,))
        return cur.fetchall()

def select_tasks_by_title(conn, title):
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM tasks WHERE title = %s", (title,))
        return cur.fetchall()

def update_task(conn, task_id, title, is_completed):
    with conn.cursor() as cur:
        cur.execute("UPDATE tasks SET title = %s, is_completed = %s WHERE task_id = %s", (title, is_completed, task_id))
        conn.commit()

def delete_task(conn, task_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM tasks WHERE task_id = %s", (task_id,))
        conn.commit()

def update_user(conn, user_id, username, password):
    with conn.cursor() as cur:
        cur.execute("UPDATE users SET username = %s, password = %s WHERE user_id = %s", (username, password, user_id))
        conn.commit()

def delete_user(conn, user_id):
    with conn.cursor() as cur:
        cur.execute("DELETE FROM users WHERE user_id = %s", (user_id,))
        conn.commit()

# Connection to the PostgreSQL database
conn = psycopg2.connect("dbname=python_web user=postgres password=adminadmin host=localhost")

# Example usage
if __name__ == '__main__':
    insert_users(conn, [("alice", sha1('password123'.encode()).hexdigest()), ("bob", sha1('password456'.encode()).hexdigest())])
    insert_tasks(conn, [("Task 1", date.today(), False, 1), ("Task 2", date.today(), True, 2)])

    print(select_users_by_id(conn, 1))
    print(select_tasks_by_title(conn, "Task 1"))

    update_task(conn, 1, "Updated Task 1", True)
    delete_task(conn, 2)
    delete_user(conn, 2)

    # Close the connection
    conn.close()
