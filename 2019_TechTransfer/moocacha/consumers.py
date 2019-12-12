# chat/consumers.py
from channels.generic.websocket import WebsocketConsumer
from . import gcpapi
from django.conf import settings
from .const import *                    
import json
import os

#AIML part
import aiml         
script_file_path = os.path.join(settings.MEDIA_ROOT, 'script/')
aiml_file_path = os.path.join(settings.MEDIA_ROOT, 'aiml/')
#new parameter
def findWordTime(word, currentVideoTime, front, scriptFile):
    # 스크립트에서 단어의 시간을 찾는 함수
    # word : 내가 찾고자 하는 단어의
    # currentVideoTime : 현재 영상 시간 --> 이 앞에서만 찾기 위해서

    timeWordList = list()

    # load json file
    # script file
    with open(scriptFile,'r', encoding='utf8') as f:
        data = json.load(f)

    if word in data['inverted_idx'].keys():
        # 검색하고자 하는 단어가 있는 경우
        for i in range(len(data['inverted_idx'][word])):
            wordTime = float(data['inverted_idx'][word][i])
            if(wordTime <= currentVideoTime):
                timeWordList.append(wordTime)
    else:
        # 검색하고자 하는 단어가 없는 경우
        pass

    if len(timeWordList) == 0:
        return currentVideoTime

    if front == True:
        return timeWordList[0]
    else:
        return timeWordList[-1]          
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        front = False
        response = dict()
        text_data_json = json.loads(text_data)
        # videoTitle
        videoTitle = text_data_json['videoName']
        # script file for current video
        scriptFile = script_file_path + videoTitle + '.json'
        aimlFile = aiml_file_path + videoTitle +'.aiml'
        k = aiml.Kernel()
        k.learn(aimlFile)
        msg = text_data_json['message'].split()
        lastWord = msg.pop()
        if lastWord in STEP_WORDS:
            for point in FIRST_POINT:
                if point in text_data_json['message']:
                    front = True
                    break;
            if front == True:
                searchingWord = msg.pop()
                searchingWord = msg.pop()
            else:
                searchingWord = msg.pop()

            timeShift = findWordTime(searchingWord, text_data_json['time'], front, scriptFile)
            if timeShift == text_data_json['time']:
                # 단어가 없거나 아직 안나온 경우
                response["message"] = 'Bot: 이 단어가 아직 나오지 않았거나 이 영상에서 없습습니다.' 
            else: # 단어를 찾은 경우
                response["message"] = 'Bot: 요청하신 단어를 찾았습니다.'
            response["timeShift"] = timeShift
            self.send(json.dumps(response))
        else:
            # AIML을 사용하는 부분
            aiml_respond = k.respond(text_data_json['message'])
            response["message"] = 'Bot : ' + aiml_respond
            response["timeShift"] = text_data_json['time']
            self.send(json.dumps(response))
            
class Default_ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = 'Bot : ' + text_data_json['message']

        self.send(text_data=json.dumps({
            'message': message
        }))
