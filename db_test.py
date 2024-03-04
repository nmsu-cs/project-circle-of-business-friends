import sqlite3
import configparser
import os

config = configparser.ConfigParser()
config.read('config.ini')

db_path = config['database']['db_path']
db_path = os.path.expandvars(db_path)

conn = sqlite3.connect(db_path)

cursor = conn.cursor()

create_table = '''
CREATE TABLE users (
ID INTEGER PRIMARY KEY AUTOINCREMENT,
username TEXT NOT NULL UNIQUE,
email TEXT NOT NULL UNIQUE,
password TEXT NOT NULL,
firstName TEXT NOT NULL,
lastName TEXT NOT NULL
);
'''
conn.execute(create_table)
conn.commit()

insert_query = '''
INSERT INTO users (username, password,email, firstName, lastName)
VALUES (?, ?, ?, ?, ?)
'''

data = ('aggies', 'aggies123*','bob@nmsu.edu', 'Bob', 'Burgers')

cursor.execute(insert_query, data)
conn.commit()

column_names_query = "PRAGMA table_info(users)"
cursor.execute(column_names_query)

columns = cursor.fetchall()

print("Column names:")
for col in columns:
    print(col[1])

select = ("SELECT * from users")

cursor.execute(select)
rows = cursor.fetchall()

print("\nContents:")
for row in rows:
    print(row)

conn.close()
