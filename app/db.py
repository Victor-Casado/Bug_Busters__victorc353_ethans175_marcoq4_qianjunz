import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

DB_FILE="onceuponatable.db"
db = sqlite3.connect(DB_FILE) #open if file exists, otherwise create
c = db.cursor()               #facilitate db ops -- you will use cursor to trigger db events
latestUID = -1
latestSID = -1

#Creating three tables
c.execute("CREATE TABLE userInfo (userID INTEGER, username TEXT, password TEXT);")
c.execute("CREATE TABLE storyInfo (storyID INTEGER, title TEXT, mainText TEXT, latestEntry TEXT, creator INTEGER);")
c.execute(f'CREATE TABLE storiesContributed (userID INTEGER);')

#Functions that add data
def addStoryColumn(storyID): #Called in the addStory function. Add column to storiesContributed corresponding to latestSID
    c.execute(f"ALTER TABLE storiesContributed ADD \'{storyID}\' INTEGER")
def addContribs(userID):
    vals = f"INSERT INTO storiesContributed VALUES({userID}"
    print ("latestSID: " + str(latestSID))
    if latestSID >= 0:
        vals += ", "
    for i in range(latestSID + 1):
        vals += "0"
        if i < latestSID:
            vals += ", "
    vals += ")"
    print("Final execute: " + vals)
    c.execute(vals)
def updateContribs(userID, storyID): #Called in the addStory function to update data value to a 1. Will also be called in __init__.py when user outside of creator adds something
    c.execute(f"UPDATE storiesContributed SET \'{storyID}\' = 1 WHERE userID = {userID}")
def addUser(username, password): #Called by __init__.py when user signs up
    global latestUID
    latestUID += 1
    c.execute(f"INSERT INTO userInfo VALUES({latestUID}, '{username}', '{password}')")
    addContribs(userID)
def addStory(storyID, title, mainText, latestEntry, creator): #Called by __init__.py when new story is created
    global latestSID
    latestSID += 1
    c.execute(f"INSERT INTO storyInfo VALUES({latestSID}, '{title}', '{mainText}', '{latestEntry}', '{creator}')")
    addStoryColumn(storyID)
    updateContribs(creator, storyID)
def updateStory(storyID, newText): #Called by __init__.py when new user makes an update to a story
    res = c.execute(f"SELECT mainTEXT FROM storyInfo WHERE storyID = {storyID}")
    mainText = list(res.fetchone())[0]
    #print(mainText)
    newMainText = mainText + newText
    c.execute(f"UPDATE storyINFO SET latestEntry = '{newText}', mainText = '{newMainText}' WHERE storyID = {storyID}")

#Functions that get data. Will all be called by __init__.py directly

#userInfo get functions
def getPassword(userID):
    res = c.execute(f"SELECT password FROM userInfo WHERE userID = {userID}")
    return (list(res.fetchone())[0])
def getUsername(userID):
    res = c.execute(f"SELECT username FROM userInfo WHERE userID = {userID}")
    return (list(res.fetchone())[0])
#storyInfo get functions
def getTitle(storyID):
    res = c.execute(f"SELECT title FROM storyInfo WHERE storyID = {storyID}")
    return (list(res.fetchone())[0])
def getMainText(storyID):
    res = c.execute(f"SELECT mainText FROM storyInfo WHERE storyID = {storyID}")
    return (list(res.fetchone())[0])
def getLatestEntry(storyID):
    res = c.execute(f"SELECT latestEntry FROM storyInfo WHERE storyID = {storyID}")
    return (list(res.fetchone())[0])
def getCreator(userID):
    res = c.execute(f"SELECT creator FROM storyInfo WHERE storyID = {storyID}")
    return (list(res.fetchone())[0])
#storiesContributed get functions
def hasWritten(userID, storyID): #Will return 1 as an integer or null
    res = c.execute(f"SELECT \'{storyID}\' FROM storiesContributed WHERE userID = {userID}")
    return (list(res.fetchone())[0])

#Test Functions: Will be commented when testing is finished
addUser('Maqarov', 'Ghidorah')
addUser('Tyson', 'Mike')
addStory('TheBeginning', 'This is the beginning', 'beginning', 0)
addStory('TheEnd', 'This is the end', 'the end', 1)
updateStory(1, ' Hold your breath and count to ten')
print(getPassword(0))
print(hasWritten(0, 1))


db.commit()
db.close()