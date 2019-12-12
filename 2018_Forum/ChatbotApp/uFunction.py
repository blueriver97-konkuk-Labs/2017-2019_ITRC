# User Function

import re
import json
import threading
import time
import urllib
from konlpy.tag import Mecab
from .uClass import *


def getText(content):
   
    PROTOCOL = 'http://'
    IP = '114.70.21.89'
    SERVICE = '/ocr/ocr.php'
    texts = ''
    MakeURL = lambda protocol, ip, service, content : '%s%s%s?url=%s' % (protocol, ip, service, content)

    url = MakeURL(PROTOCOL, IP, SERVICE, content)

    with urllib.request.urlopen(url) as url:
        # JSON Object
        #data = json.loads(url.read().decode('utf-8'))
        # String Object
        data = url.read().decode('utf-8')
    
    texts = data
    #print(texts)
    return texts

def getInfo(dataset, content, msgType):

    tagFlag = {}
    payloadObj = {}
    content = " ".join(content)
    #print(content)
    if msgType == "TEXT":
        for tag in dataset.tag.keys():
            for word in dataset.tag[tag]:
                if word in content:
                    tagFlag[tag] = word
                    break;

        # general case processing     
        for tag in tagFlag.keys():
            if (tag == "contents"):
                payloadObj[tag] = dataset.data[tag]
            elif (tag == "name"):
                payloadObj[tag] = dataset.data[tag]
            elif (tag == "location"):
                payloadObj[tag] = dataset.data[tag]
            elif (tag == "title"):
                payloadObj[tag] = dataset.data[tag]
            elif (tag == "url"):
                payloadObj[tag] = dataset.data[tag]
            else: # univ, center, groups
                payloadObj[tag] = tagFlag[tag]
        
        # special case processing
        if ("univ" not in tagFlag) and ("center" not in tagFlag) and (len(tagFlag.keys()) != 0):
            payloadObj["univ"] = "건국대학교 인공지능 클라우드 연구센터"

        if ("contents" in tagFlag) and ("groups" in tagFlag):
            group = 'group%c' % ((tagFlag["groups"])[0])
            payloadObj["contents"] = dataset.data["groups"][group]["contents"]

        if ("name" in tagFlag) and ("groups" in tagFlag):
            group = 'group%c' % ((tagFlag["groups"])[0])
            payloadObj["name"] = "%s" % (dataset.data["groups"][group]["name"])
        
        if ("title" in tagFlag) and ("groups" in tagFlag):
            group = 'group%c' % ((tagFlag["groups"])[0])
            payloadObj["title"] = "%s" % (dataset.data["groups"][group]["title"])

        # word relevance comparison processing
        if ("keyword" in tagFlag):
            numMax = 0
            matchList = list()
            for group in dataset.data["groups"].keys():
                cnt = 0
                wordList = dataset.data["groups"][group]["keyword"]
                #print(wordList)
                for word in wordList:
                    if word in content:
                        cnt += 1
                if (cnt/len(wordList)) > numMax:
                    #print(cnt/len(wordList))
                    numMax = cnt/len(wordList)
                    matchList.append(group)
            #print(matchList) 
            if len(matchList) > 0:
                payloadObj["contents"] = "이 내용이 가장 적절해 보여요 \n\n%s" % (dataset.data["groups"][matchList[-1]]["contents"])
            else:
                payloadObj["contents"] = "관련 내용이 없는것 같아요."

    elif msgType == "IMAGE":
        numMax = -1
        matchList = list()
        for group in dataset.data["groups"].keys():
            cnt = 0
            wordList = dataset.data["groups"][group]["keyword"]
            for word in wordList:
                if word in content:
                    cnt += 1
            if (cnt/len(wordList)) >= numMax:
                #print(cnt/len(wordList))
                numMax = cnt/len(wordList)
                matchList.append(group)
        
        if len(matchList) > 1:
            payloadObj["contents"] = dataset.data["groups"][matchList[-1]]["contents"]
        else:
            payloadObj["contents"] = "관련 내용이 없는것 같아요."
        
    else:
        print("처리할 수 없는 타입입니다.")

    #print(tagFlag)
    #print(payloadObj)
    return payloadObj

def getKeyword(content, msgType):
   
    mecab = Mecab()
    if msgType == "TEXT":
        parseStr = mecab.morphs(content)
    elif msgType == "IMAGE":
        parseStr = mecab.nouns(content)
    else:
        pass

    #print(parseStr)
    return parseStr

