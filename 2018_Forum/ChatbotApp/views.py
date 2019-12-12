# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

import re
import time
import json
import threading
import datetime

from .uClass import *
from .uFunction import *
# Create your views here.


#################################################
#                                               #
#   ChatbotApp :: CONST / GLOBAL                #
#                                               #
#################################################
users = {}
dataset = Dataset()
NLP = True

#################################################
#                                               #
#   ChatbotApp :: funtions                      #
#                                               #
#################################################

def JsonKbDefault(*btn):
    return JsonResponse({
        "type" : "buttons",
        "buttons" : list(btn)
    })

def JsonMsgNull():
    return JsonResponse({})

def JsonMsgText(msg):
    return JsonResponse({
        "message" : {
            "text" : msg    
        },
        "keyboard" : {
            "type" : "text"
        }
    })

def JsonMsgButton(msg, *btn):
    return JsonResponse({
        "message" : {
            "text" : msg
        },
        "keyboard" : {
            "type" : "buttons",
            "buttons" : list(btn)
        }
    })

def JsonPhotoText(msg, url, width, height):
    return JsonResponse({
        "message" : {
            "text" : msg,
            "photo" : {
                "url" : url,
                "width" : width,
                "height" : height
            }   
        },
        "keyboard" : {
            "type" : "text"
        }
    })

def JsonPhotoButton(msg, url, width, height, label, btn_url):
    return JsonResponse({
        "message" : {
            "text" : msg,
            "photo" : {
                "url" : url,
                "width" : width,
                "height" : height
            },
            "message_button" : {
                "label" : label,
                "url" : btn_url
            }
        },
        "keyboard" : {
            "type" : "text"
        }
    })

def processMsg(user, content):

    pattern1 = re.compile('\s+')
    pattern2 = re.compile('^http://')
    payload = ''
    answer = ''
    
    content = re.sub(pattern1, '', content)
    #print(content)
    if pattern2.search(content):
        user.msgType = 'IMAGE'
        print('user message type : ', user.msgType)
        
        result = getText(content)
        if NLP == True:
            parseStr = getKeyword(result, user.msgType)
            result = list(set(parseStr))

    else:
        user.msgType = 'TEXT'
        print('user message type : ', user.msgType)
        
        result = content
        if NLP == True:
            parseStr = getKeyword(content, user.msgType)
            result = parseStr
    
    payloadObj = getInfo(dataset, result, user.msgType)
    
    # answer making
    #print(payloadObj.keys())
    #print(payloadObj)
    
    if "contents" in payloadObj:
        answer = payloadObj["contents"]
    if "groups" in payloadObj:
        if ("univ" in payloadObj) and ("groups" in payloadObj )and ("name" in payloadObj):
            answer = "%s %s에서 진행중인 연구는 %s 입니다." % (payloadObj["univ"], payloadObj["groups"], payloadObj["name"])
        elif ("univ" in payloadObj) and ("groups" in payloadObj) and ("title" in payloadObj):
            answer = "%s %s의 전시 내용은 %s 입니다." % (payloadObj["univ"], payloadObj["groups"], payloadObj["title"])
        else:
            pass
    else:    
        if ("univ" in payloadObj) and ("location" in payloadObj):
            answer = "%s 전시 위치는 %s 입니다." % (payloadObj["univ"], payloadObj["location"])
            img = "http://114.70.21.96%s" % (dataset.data["img"][1])
            return JsonPhotoText(answer, img, 640, 640)
        elif ("univ" in payloadObj) and ("url" in payloadObj):
            answer = "CLAIR 웹 주소 보내드려요~ \n %s" % (payloadObj["url"])
        elif ("univ" in payloadObj) and ("groups" in payloadObj )and ("name" in payloadObj):
            answer = "%s %s에서 진행중인 연구는 %s 입니다." % (payloadObj["univ"], payloadObj["groups"], payloadObj["name"])
        elif ("univ" in payloadObj) and ("title" in payloadObj):
            answer = "%s의 주제는 %s 입니다." % (payloadObj["univ"], payloadObj["title"])
        else:
            pass

    if answer == '':
        answer = '잘 모르겠어요. 다른 질문을 해주실래요?'
#    # message formatting
#    if isinstance(payload, list):
#        for k in payload:
#            answer += '%s ' % (k)
#    elif isinstance(payload, str):
#        answer = payload

    return JsonMsgText(answer)

#################################################
#                                               #
#   Kakao TALK :: Plus Friends - Develope APIs  #
#                                               #
#################################################
START = "버튼을 누르면 시작됩니다"
FIRST = "질문이나 사진을 입력해주세요~"
def keyboard(request) : 
    return JsonKbDefault(START)

@csrf_exempt
def message(request) :
    currentMessage = (request.body).decode('utf-8')
    jsonStr = json.loads(currentMessage)
    userKey = jsonStr['user_key']
    content = jsonStr['content']
    print(userKey, content)

    if(userKey in users) == False:
        users[userKey] = User(userKey)
    user = users[userKey]

    if content == START:
        user.answerList.clear()
        return JsonMsgText(FIRST)
    else:
        return processMsg(user, content)


@csrf_exempt
def chat_room(request) :
    return JsonMsgNull()
