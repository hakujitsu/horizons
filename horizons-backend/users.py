USERS = dict()

class User:
    def __init__(self, age_range, location, bias):
        self._age_range = age_range
        self._location = location
        self._political_bias = (bias, 0.0, 0)
        self._history = list()
        self._opinion = dict()

    def get_age_range(self):
        return self._age_range

    def get_history(self):
        return self._history

    def update_history(self, value):
        self._history.append(value)
        pb = list(self._political_bias)
        pb[2] = pb[2] + 1
        self._political_bias = tuple(pb)

    def get_political_bias(self):
        return self._political_bias

    def update_political_bias(self, value):
        self._political_bias = value

    def get_opinion(self):
        return self._opinion

    def update_opinion(self, value):
        self._opinion = value

    def printDetails(self):
        print(self._age_range)
        print(self._location)
        print(self._political_bias)
        print(self._history)
        print(self._opinion)


def addUserToDict(age, location, politics):
    bias = 0
    if (politics == "left"):
       bias = -4
    elif (politics == "center-left"):
       bias = -2
    elif (politics == "center-right"):
       bias = 2
    elif (politics == "right"):
       bias = 4

    currLen = len(USERS)
    user = User(age, location, bias)
    USERS[currLen] = user
    return currLen

def addMockUserToDict():
    currLen = len(USERS)
    user = User('18-29', 'USA', -2)
    USERS[currLen] = user
    return currLen

def getUserFromDict(user_id):
    return USERS[user_id]

def updateUserHistory(user_id, url):
    user = getUserFromDict(user_id)
    user.update_history(url)
