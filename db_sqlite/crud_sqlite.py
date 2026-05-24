import sqlite3
from hashlib import sha1

from datetime import datetime

def connect_db():
    return sqlite3.connect('python_web.db')

def insert_users(user_data):
    conn = connect_db()
    cur = conn.cursor()
    cur.executemany('INSERT INTO users (username, password) VALUES (?,?)', user_data)
    conn.commit()
    conn.close()

def select_user_by_id(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE user_id=?', (user_id,))
    user = cur.fetchone()
    conn.close()
    return user

def select_user_by_username(username):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username=?', (username,))
    user = cur.fetchone()
    conn.close()
    return user

def insert_tasks(task_data):
    conn = connect_db()
    cur = conn.cursor()
    cur.executemany('INSERT INTO tasks (title, created_at, is_completed, user_id) VALUES (?, ?, ?, ?)', task_data)
    conn.commit()
    conn.close()

def select_task_by_id(task_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks where task_id=?', (task_id,))
    task = cur.fetchone()
    conn.close()
    return task

def select_task_by_title(title):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('SELECT * FROM tasks WHERE title=?', (title,))
    task = cur.fetchone()
    conn.close()
    return task

def update_task(task_id, title, is_completed):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('UPDATE tasks SET title=?, is_completed=? WHERE task_id=?', (title, is_completed, task_id))
    conn.commit()
    conn.close()

def delete_task(task_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM tasks WHERE task_id=?', (task_id,))
    conn.commit()
    conn.close()

def update_user(user_id, username, password):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('UPDATE users SET username=?, password=? WHERE user_id=?', (username, sha1(password.encode()).hexdigest(), user_id))
    conn.commit()
    conn.close()

def delete_user(user_id):
    conn = connect_db()
    cur = conn.cursor()
    cur.execute('DELETE FROM users WHERE user_id=?', (user_id,))
    conn.commit()
    conn.close()


if __name__ == '__main__':
    insert_users(
        [('Alice', sha1('password123'.encode()).hexdigest()), ('Bob', sha1('password456'.encode()).hexdigest())])
    insert_tasks([('Task 1', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0, 1), ('Task 2', datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 0, 2)])
    print(select_user_by_id(1))
    print(select_task_by_title('Task 1'))
    update_task(1, 'Updated Task 1', 1)
    delete_user(2)