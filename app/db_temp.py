import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

DB_FILE="temptable.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events

c.execute("CREATE TABLE userInfo (userID INTEGER, username TEXT, password TEXT);")
c.execute("CREATE TABLE storyInfo (storyID INTEGER, title TEXT, mainText TEXT, latestEntry TEXT, creator INTEGER);")
def storiesColumn(): #Helps create the storiesColumn table by looping thorugh current number of storyIDs
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
c.execute(f'CREATE TABLE storesContributed (username TEXT{storiesColumn()});')
