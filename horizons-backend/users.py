USERS = dict()

def addUserToDict(age, location, politics):
    user = {"age": age, "location": location, "politics": politics, "history": list()}
    currLen = len(USERS)
    USERS[currLen] = user
    return currLen

def getUserFromDict(user_id):
    return USERS[user_id]

def updateUserHistory(user_id, url):
    user = getUserFromDict(user_id)
    user["history"].append(url)

