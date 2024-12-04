import psycopg2

conn = psycopg2.connect("dbname=healthmate user=postgres password=galena2612")
cursor = conn.cursor()
cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
print(cursor.fetchall())
conn.close()
