import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

DB_FILE="onceuponatable.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

c.execute("CREATE TABLE userInfo (userID INTEGER, username TEXT, password TEXT);")
c.execute("CREATE TABLE storyInfo (storyID INTEGER, title TEXT, mainText TEXT, latestEntry TEXT, creator INTEGER);")
def addUser():
    c.execute("""
        INSERT INTO userInfo VALUES
        (0, 'Maqarov', 'Ghidorah'),
        (1, 'Maqro Man', 'Gojira')
    """)
def addStory():
    c.execute("""
        INSERT INTO storyInfo VALUES
        (0, 'TheBeginning', 'This is the beginning', 'beginning', 'Maqarov'),
        (1, 'TheEnd', 'This is the end', ' the end', 'Maqro Man')
    """)
addUser()
addStory()
def storiesColumn():
    fin = ""
    storyIDs = c.execute("SELECT storyID FROM storyInfo")
    listIDs = storyIDs.fetchall()
    print(listIDs)
    if len(listIDs) == 0:
        fin += ", "
    for i in range(len(listIDs)):
        fin += f'{list(listIDs[i])[0]} TEXT'
        if i != len(listIDs) - 1:
            fin += ", "
    return fin
print(storiesColumn())
c.execute(f'CREATE TABLE storesContributed (userID INTEGER);')
latestUID = 0
latestUID = 0

db.commit()
db.close()