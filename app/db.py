import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

DB_FILE="onceuponatable.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
latestUID = -1
latestSID = -1

c.execute("CREATE TABLE userInfo (userID INTEGER, username TEXT, password TEXT);")
c.execute("CREATE TABLE storyInfo (storyID INTEGER, title TEXT, mainText TEXT, latestEntry TEXT, creator INTEGER);")
c.execute(f'CREATE TABLE storiesContributed (userID INTEGER);')
def addStoryColumn(storyID):
    c.execute(f"ALTER TABLE storiesContributed ADD {storyID} INTEGER")
def addContribs(userID):
    vals = f"INSERT INTO storiesContributed VALUES({userID}"
    if latestSID >= 0:
        vals += ", "
    for i in range(latestSID + 1):
        vals += "0"
        if i < latestSID:
            vals += ", "
    vals += ")"
    print(vals)
    c.execute(vals)
def updateContribs(userID, storyID):
    c.execute(f"UPDATE storiesContributed SET \'{storyID}\' = 1 WHERE userID = {userID}")
def addUser(userID, username, password):
    userID += 1
    global latestUID
    latestUID = userID
    c.execute(f"INSERT INTO userInfo VALUES({userID}, '{username}', '{password}')")
    addContribs(userID)
def addStory(storyID, title, mainText, latestEntry, creator):
    storyID += 1
    global latestSID
    latestSID = storyID
    c.execute(f"INSERT INTO storyInfo VALUES({storyID}, '{title}', '{mainText}', '{latestEntry}', '{creator}')")
    c.execute(f"UPDATE storiesContributed SET \'{storyID}\' = 1 WHERE userID = {creator}")
    updateContribs(creator, storyID)

addUser(latestUID, 'Maqarov', 'Ghidorah')
addUser(latestUID, 'Tyson', 'Mike')
addStory(latestSID, 'TheBeginning', 'This is the beginning', 'beginning', 0)
addStory(latestSID, 'TheEnd', 'This is the end', 'the end', 1)


db.commit()
db.close()