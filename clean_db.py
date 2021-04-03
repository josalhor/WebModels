import os

db='db.sqlite3'

if os.path.isfile(db):
    os.remove(db)