task_storage = {}
users = {}

import sqlite3

conn_obj = sqlite3.connect('python_web.db')
conn_obj.close()