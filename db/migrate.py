import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cemiterios = []
with open('nomes_cemiterios.txt', encoding='utf-8') as f:
    cemiterios = [x.strip() for x in f.readlines()]

# print(cemiterios)
cursor.execute("DROP TABLE IF EXISTS TBCemiterios")
conn.commit()
cursor.execute('''CREATE TABLE TBCemiterios (ID INTEGER PRIMARY KEY AUTOINCREMENT, Nome TEXT)''')
conn.commit()

for cem in cemiterios:
    cursor.execute(f"INSERT INTO TBCemiterios (Nome) VALUES ('{cem}')")
conn.commit()

cursor.execute("SELECT * FROM TBCemiterios")
print(cursor.fetchall())

# cursor.execute("SELECT * FROM TBCemiterios WHERE ID > 10")
# rv = cursor.fetchall() 
# if len(rv) > 0:
#     print(rv)
# else:
#     print("Not found.")


# Commit the changes
# conn.commit()

conn.close()