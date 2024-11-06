import sqlite3   #enable control of an sqlite database
import csv       #facilitate CSV I/O

DB_FILE="onceuponatable.db"
latestUID = -1
latestSID = -1

#Creating three tables
def createTables():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute("CREATE TABLE userInfo (userID INTEGER, username TEXT, password TEXT);")
    c.execute("CREATE TABLE storyInfo (storyID INTEGER, title TEXT, mainText TEXT, latestEntry TEXT, creator INTEGER);")
    c.execute(f'CREATE TABLE storiesContributed (userID INTEGER);')
    db.commit()
    db.close()

#Functions that add data

#Helper functions
def addStoryColumn(storyID): #Called in the addStory function. Add column to storiesContributed corresponding to latestSID
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute(f"ALTER TABLE storiesContributed ADD '{storyID}' INTEGER")
    c.execute(f"UPDATE storiesContributed SET '{storyID}' = 0")
    db.commit()
    db.close()
def addContribs(userID): #Called in addUser function.
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    fin = f"INSERT INTO storiesContributed VALUES({userID}"
    if latestSID > -1:
        fin += ", "
    for i in range(latestSID + 1):
        #print("Current iteration: " + str(i))
        fin += "0"
        if i < latestSID:
            fin += ", "
    fin += ")"
    print(fin)
    c.execute(fin)
    db.commit()
    db.close()
def updateContribs(userID, storyID): #Called in the addStory and updateStory functions to update data value to a 1.
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    c.execute(f"UPDATE storiesContributed SET '{storyID}' = 1 WHERE userID = {userID}")
    db.commit()
    db.close()

#Functions called by __init__.py
def addUser(username, password): #Called by __init__.py when user signs up
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    global latestUID
    latestUID += 1
    #print("latest UID (printed from addUser): " + str(latestUID))
    c.execute(f"INSERT INTO userInfo VALUES({latestUID}, '{username}', '{password}')")
    db.commit()
    db.close()
    addContribs(latestUID)
def getLatestUID():
    return latestUID
def getLatestSID():
    return latestSID
def addStory(title, mainText, latestEntry, creator): #Called by __init__.py when new story is created
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    global latestSID
    latestSID += 1
    c.execute(f"INSERT INTO storyInfo VALUES({latestSID}, '{title}', '{mainText}', '{latestEntry}', {creator})")
    db.commit()
    db.close()
    addStoryColumn(latestSID)
    updateContribs(creator, latestSID)
    #print("latest SID: " + str(latestSID))
def updateStory(storyID, newText, creator): #Called by __init__.py when new user makes an update to a story
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    res = c.execute(f"SELECT mainTEXT FROM storyInfo WHERE storyID = {storyID}")
    mainText = list(res.fetchone())[0]
    #print(mainText)
    newMainText = mainText + newText
    c.execute(f"UPDATE storyINFO SET latestEntry = '{newText}', mainText = '{newMainText}', creator = {creator} WHERE storyID = {storyID}")
    db.commit()
    db.close()
    updateContribs(creator, storyID)


#Functions that get data. Will all be called by __init__.py directly

#userInfo get functions
def getPassword(userID):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    res = c.execute(f"SELECT password FROM userInfo WHERE userID = {userID}")
    fin = list(res.fetchone())[0]
    db.commit()
    db.close()
    return (fin)
def getUsername(userID):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    res = c.execute(f"SELECT username FROM userInfo WHERE userID = {userID}")
    fin = list(res.fetchone())[0]
    db.commit()
    db.close()
    return (fin)
def allUserData():
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    res = c.execute(f"SELECT * FROM userInfo")
    userList = res.fetchall()
    userDict = {}
    for i in range(len(userList)):
        userDict[list(userList[i])[0]] = [list(userList[i])[1], list(userList[i])[2]]
    db.commit()
    db.close()
    return (userDict)
#storyInfo get functions
def getTitle(storyID):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    res = c.execute(f"SELECT title FROM storyInfo WHERE storyID = {storyID}")
    fin = list(res.fetchone())[0]
    db.commit()
    db.close()
    return (fin)
def getMainText(storyID):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    res = c.execute(f"SELECT mainText FROM storyInfo WHERE storyID = {storyID}")
    fin = list(res.fetchone())[0]
    db.commit()
    db.close()
    return (fin)
def getLatestEntry(storyID):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    res = c.execute(f"SELECT latestEntry FROM storyInfo WHERE storyID = {storyID}")
    fin = list(res.fetchone())[0]
    db.commit()
    db.close()
    return (fin)
def getCreator(userID):
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    res = c.execute(f"SELECT creator FROM storyInfo WHERE storyID = {storyID}")
    fin = list(res.fetchone())[0]
    db.commit()
    db.close()
    return (fin)
#storiesContributed get functions
def hasWritten(userID, storyID): #Will return 1 as an integer or null
    db = sqlite3.connect(DB_FILE, check_same_thread=False)
    c = db.cursor()
    res = c.execute(f"SELECT * FROM storiesContributed")
    #cur = db.cursor()
    #print(cur.fetchall())
    fin = list(res)
    db.commit()
    db.close()
    return (fin[userID][storyID+1])

def getStoriesArray(): #used by homepage
    i = 0
    array = []
    while i <= latestSID:
        array.append([getTitle(i),i])
        i+=1
    return array

#Test Functions: Will be commented when testing is finished
'''
createTables()
addUser('Maqarov', 'Ghidorah')
addUser('Tyson', 'Mike')
addStory('TheBeginning', 'This is the beginning', 'beginning', 0)
addStory('TheEnd', 'This is the end', 'the end', 1)
addUser('KSI', 'Thick of It')
updateStory(1, ' Hold your breath and count to ten', 1)
print(getPassword(0))
print(str(hasWritten(0, 0)))
print(str(hasWritten(1, 1)))
print(str(hasWritten(2, 1)))
print(allUserData())'''

