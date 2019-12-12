# User Class.py

import json
import os

class Dataset:
    
    def __init__(self):
        self.data = {}
        self.tag = {}
        
        # initial dataset parsing
        path = os.path.dirname(os.path.realpath(__file__))
        target = path + '/resources/data.json'
        with open(target, 'r') as f:
            Object = json.load(f)["data"]

            for tag in Object.keys():
                if tag == "groups":
                    self.data[tag] = {}
                    for t in Object[tag].keys():
                        self.data[tag][t] = Object[tag][t]
                else:
                    self.data[tag] = Object[tag]
        #print(self.data)

        path = os.path.dirname(os.path.realpath(__file__))
        target = path + '/resources/tag.json'
        with open(target, 'r') as f:
            Object = json.load(f)["tag"]

            for t in Object.keys():
                self.tag[t] = Object[t]
        #print(self.tag)

        # contents replace
        target = path + self.data["contents"]
        with open(target, 'r') as f:
            self.data["contents"] = f.read()
                
        groupList = self.data["groups"].keys()
        for group in groupList:
            target = path + self.data["groups"][group]["contents"]
            with open(target, 'r') as f:
                self.data["groups"][group]["contents"] = f.read()

        #print(self.data) 

class User:
    # class var
    count = 0

    # init Method
    def __init__(self, userKey):
        self.userKey = userKey
        self.answerList = list()
        self.msgType = -1
        self.msgOrder = -1
        
