import sqlite3

con = sqlite3.connect("./db.sqlite3")

con.execute("""CREATE TABLE IF NOT EXISTS test
            (
    ID INTEGER NOT NULL PRIMARY KEY,
    text TEXT
)
            """)
con.execute("""INSERT INTO test (text) VALUES (?)""", ("Une texte",))  # Specify the column name in INSERT
con.commit()
con.close()