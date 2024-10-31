import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

DB_FILE="onceuponatable.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
latestUID = 0
latestSID = 0

c.execute("CREATE TABLE userInfo (userID INTEGER, username TEXT, password TEXT);")
c.execute("CREATE TABLE storyInfo (storyID INTEGER, title TEXT, mainText TEXT, latestEntry TEXT, creator INTEGER);")
def storiesColumn():
    fin = ""
    storyIDs = c.execute("SELECT storyID FROM storyInfo")
    listIDs = storyIDs.fetchall()
    if len(listIDs) != 0:
        fin += ", "
    for i in range(len(listIDs)):
        fin += f'\'{list(listIDs[i])[0]}\' INTEGER'
        if i != len(listIDs) - 1:
            fin += ", "
    return fin
c.execute(f'CREATE TABLE storesContributed (userID INTEGER{storiesColumn()});')

def addUser(userID, username, password):
    c.execute(f"INSERT INTO userInfo VALUES({userID}, '{username}', '{password}')")
    addContribs(userID)
def addStory(storyID, title, mainText, latestEntry, creator):
    c.execute(f"INSERT INTO storyInfo VALUES({storyID}, '{title}', '{mainText}', '{latestEntry}', '{creator}')")
def addContribs(userID):
    vals = f"INSERT INTO storiesContributed (userID"
    if  != 0:
        vals
    c.execute(vals) 
addUser(latestUID, 'Maqarov', 'Ghidorah')
addStory(latestSID, 'TheBeginning', 'This is the beginning', 'beginning', 'Maqarov')


db.commit()
db.close()