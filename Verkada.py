#!/usr/bin/env python

import json
import sys

import requests
import re
# Import any libraries you need
## Do not edit
class VerkadaDB():
    def __init__(self):
        self._data = {}

#class for user
class user:
    def __init__(self, name, domain, topLevelName, age, gender, nationality):
        self.age = age
        self.gender = gender
        self.nationality = nationality
        self.name = name
        self.domain = domain
        self.topLevelName = topLevelName

#class for final answer
class finalAns:
    def __init__(self, name, queryDataAsJSON, dataBaseContentsAsJSON, responseToQ1, responseToQ2):
        self.name = name
        self.queryDataAsJSON = queryDataAsJSON
        self.dataBaseContentsAsJSON = dataBaseContentsAsJSON
        self.responseToQ1 = responseToQ1
        self.responseToQ2 = responseToQ2

## Do not edit   
dbInstance = VerkadaDB()

## To-do: Implement Function (mimics AWS Lambda handler)
## Input: JSON String which mimics AWS Lambda input


def lambda_handler(json_input):
    #fetching email, name, domain, and topLevelName
    email = json.loads(json_input)['email']
    name = getName(email)
    domain = getDomain(email)
    topLevelName = getTopLevelName(email)

    if(domain == "verkada"):
        return

    #using APIs to fetch age, gender, and nationality
    age = get_age(name)
    gender = get_gender(name)
    nationality = get_nationality(name)

    #creating new user
    newUser = user(name, domain, topLevelName, age, gender, nationality)
    addUser(newUser)

    json_output = json.dumps({})
    ## Output: JSON String which mimics AWS Lambda Output
    return json_output

#functions to make API calls and extract information
def get_age(name):
    url = "https://api.agify.io/?name=" + name
    return requests.get(url).json()['age']

def get_gender(name):
    url = "https://api.genderize.io?name=" + name
    return requests.get(url).json()['gender']

def get_nationality(name):
    url = "https://api.nationalize.io?name=" + name
    return requests.get(url).json()['country'][0]['country_id']

def getName(email):
    return email.split("@")[0]

def getDomain(email):
    return email.split("@")[1].split(".")[0]

def getTopLevelName(email):
    return email.split("@")[1].split(".")[1]

#database manipulation functions

def generateKey(age, name, gender, nationality, topLevelName, domain):
    return str(age) + "#" + name + "#" + gender + "#" + nationality + "#" + topLevelName + "#" + domain

def addUser(user):
    key = generateKey(user.age, user.name, user.gender, user.nationality, user.topLevelName, user.domain)
    dbInstance._data[key] = json.loads(json.dumps(user.__dict__))

#helper method used by queryUser, updateUser, and deleteUser
def queryHelper(name, gender, nationality, topLevelName, domain):
    #creating a key that matches with different keys of the dictionary
    key = "(.)*#"
    if(name != None):
        key = key + name + "#"

    else:
        key = key + "(.)*#"


    if(gender != None):
        key = key + gender + "#"

    else:
        key = key + "(.)*#"

    if(nationality != None):
        key = key + nationality + "#"

    else:
        key = key + "(.)*#"

    if(topLevelName != None):
        key = key + topLevelName + "#"

    else:
        key = key + "(.)*#"

    if(domain != None):
        key = key + domain

    else:
        key = key + "(.)*"

    reqex = re.compile(key)
    list = []
    for uniqueKey in dbInstance._data.keys():
        if(reqex.search(uniqueKey) != None):
            list.append(uniqueKey)

    return list

#Adding a lot of extra parameters to give more functionality.
# For example: Query all people who are male, aged between 30 and 60 and live in the US.
# The function for this example will be updateUser(None, 30, 60, "male", "US", None, None,)
def queryUser(name, ageMin, ageMax, gender, nationality, topLevelName, domain):
    listOfUserKeys = queryHelper(name, gender, nationality, topLevelName, domain)
    list = []
    for key in listOfUserKeys:
        if((ageMin == None and ageMax == None) or (dbInstance._data[key]['age'] >= ageMin and dbInstance._data[key]['age'] <= ageMax)):
            list.append(dbInstance._data[key])

    return list

#Adding a lot of extra parameters to give more functionality.
# For example: Change every Kyle who is aged between 30 and 60  and lives in the US to have a new age and nationality.
# The function for this example will be updateUser("Kyle", 30, 60, None, US, None, None, 26, None, "Bosnia")
def updateUser(name, ageMin, ageMax, gender, nationality, topLevelName, domain, newAge, newGender, newNationality):
    listOfUserKeys = queryHelper(name, gender, nationality, topLevelName, domain)
    for key in listOfUserKeys:
        if((ageMin == None and ageMax == None) or (dbInstance._data[key]['age'] >= ageMin and dbInstance._data[key]['age'] <= ageMax)):
            user = dbInstance._data[key]
            if(newAge != None):
                user['age'] = newAge
            if(newGender != None):
                user['gender'] = newGender
            if(newNationality != None):
                user['nationality'] = newNationality

            newKey = generateKey(user['age'], user['name'], user['gender'], user['nationality'], user['topLevelName'], user['domain'])
            dbInstance._data[newKey] = user
            del(dbInstance._data[key])

#This function supports a lot of functionalities. For example: Delete all users who are named Karen, live in US, and are females
#The query will for this example will be deleteUser("Karen", None, None, "female", "US", None, None)
def deleteUser(name, ageMin, ageMax, gender, nationality, topLevelName, domain):
    listOfUserKeys = queryHelper(name, gender, nationality, topLevelName, domain)
    for key in listOfUserKeys:
        if((ageMin == None and ageMax == None) or (dbInstance._data[key]['age'] >= ageMin and dbInstance._data[key]['age'] <= ageMax)):
            del(dbInstance._data[key])



#def limitFunction(listOfUsers, limit):

## Do not edit
lambda_handler(json.dumps({"email":"John@acompany.com"}))
lambda_handler(json.dumps({"email":"Kyle@ccompany.com"}))
lambda_handler(json.dumps({"email":"Georgie@dcompany.net"}))
lambda_handler(json.dumps({"email":"Karen@eschool.edu"}))
lambda_handler(json.dumps({"email":"Annie@usa.gov"}))
lambda_handler(json.dumps({"email":"Elvira@fcompay.org"}))
lambda_handler(json.dumps({"email":"Juan@gschool.edu"}))
lambda_handler(json.dumps({"email":"Julie@hcompany.com"}))
lambda_handler(json.dumps({"email":"Pierre@ischool.edu"}))
lambda_handler(json.dumps({"email":"Ellen@canada.gov"}))
lambda_handler(json.dumps({"email":"Willy@bcompany.co.uk"}))
lambda_handler(json.dumps({"email":"Craig@jcompany.org"}))
lambda_handler(json.dumps({"email":"Juan@kcompany.net"}))
lambda_handler(json.dumps({"email":"Jack@verkada.com"}))
lambda_handler(json.dumps({"email":"Jason@verkada.com"}))
lambda_handler(json.dumps({"email":"Billy@verkada.com"}))
lambda_handler(json.dumps({"email":"Brent@verkada.com"}))

## Put code for Part 2 here

updateUser("Kyle", None, None, None, None, None, None, 26, None, "Bosnia")

deleteUser("Craig", None, None, None, None, None, None)

queryList = queryUser(None, 30, sys.maxsize, "male", None, None, None)

#sorting and finding youngest 4
queryList.sort(key = lambda x: x['age'])
ans = []
for i in range(4):
    ans.append(queryList[i]['name'])

#creating final answer
name = "Vimanyu Saxena"
queryDataAsJSON = json.dumps(ans)
dataBaseContentsAsJSON = json.dumps(dbInstance._data)
responseToQ1 = "As sales representatives collect data from the customers, I would like to associate revenue generated \nwith age, gender, and nationality of the customers. For each age, gender, and nationality, I would \nalso like to get an idea of how many interations were made in total to generate the revenue. With this \ndata, we can come up with techniques to maximize revenue with the minimum number of interactions. \nSince collecting data at a national level doesn't provide detailed insights, I would like to more insights \nabout revenue generated while looking at age, name, and gender at state, county, and city specific level. \nIf we can get data about the total spending people do in a month and the type of items they purchase according to \ntheir age, gender, and location, then that can really help our system generate more money. With this information,  \nour representatives can target the right customers to generate maximum revenue, also decreasing total number of interactions \nbetween them as we know which customers want what products."
responseToQ2 = "We can use Verkada cameras outside of shopping malls and stores to detect people. We can use their images \nto extract their age and gender. After getting this information, we can extract information from \nthe shopping bag they are holding in the image and try to map a pattern between age, gender, and the \ntypes of items that the store usually sells. With this, we can target people with the items \nthat are most popular according to their age and gender. Scaling up by integrating verkada cameras outside all \nstores in a location or a country can give us a lot of location specific data that we can use for revenue \ngeneration. Another idea is to install Verkada cameras in public places so we can see which people are wearing what \nkind of clothes or using different kinds of items. We can extract items' and products' information they are using and \nmap to the age, gender and location information extracted from their image and use that for future campaigns."

finalAns = finalAns(name, queryDataAsJSON, dataBaseContentsAsJSON, responseToQ1, responseToQ2)

#creating POST API request
url = "https://rwph529xx9.execute-api.us-west-1.amazonaws.com/prod/pushToSlack"
x = requests.post(url, json.loads(json.dumps(finalAns.__dict__)))
print(x.text)


