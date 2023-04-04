USERS = dict()

def addUserToDict(age, location, politics):
    user = {age: age, location: location, politics: politics}
    currLen = len(USERS)
    USERS[currLen] = user
    return currLen

def getUserFromDict(user_id):
    return USERS[user_id]

