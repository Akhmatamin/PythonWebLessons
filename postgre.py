import psycopg2

conn_obj = psycopg2.connect(dbname='python_web',user='postgres',password='adminadmin', host='localhost', port=5432)
conn_obj.close()

