# ITRC2018-Chatbot

ITRC Forum 2018 - Chatbot Project Git repository

##### Copyright 2018, Embedded Intelligent Computing Laboratory, KonKuk Univ.

---------------------------------------
Installation Guide
---------------------------------------

#### 1. Install Python3

    $ apt-get install python3-dev

#### 2. Install python3-venv

    $ apt-get install python3-venv

#### 3. create working directory & virtual env.

    $ mkdir venv
    $ cd venv
    $ python3 -m venv itrc

#### 4. activate venv

    $ source itrc/bin/activate
	
#### *result

    (itrc)ubuntu@ubuntu:~$


#### 5. install Django

    (itrc) $ pip install --upgrade pip
    (itrc) $ pip install django


#### 6. git clone repo

    (itrc) $ git clone https://github.com/blueriver97/ITRC2018-Chatbot.git
    or
    (itrc) $ git clone git@github.com:blueriver97/ITRC2018-Chatbot.git
#### 7. change directory

    (itrc) $ cd ITRC2018-Chatbot

#### 8. run server
    
    (itrc) $ python3 manage.py runserver 0.0.0.0:8000
    
---------------------------------------

##### Commit 작성 포맷
    
    Issue# < 이슈 내용 or 작업 내용 >
    file name : 간략한 수정 내용

    example:

    Issue# 기본 파일 구성
    views.py : 기초 Kakao Talk API 추가 구현
    
    
##### Git Commit 기본 에디터 변경

    $ git config --global core.editor "vim"
    

##### Git ssh-key 등록 및 기초 사용법 정리
https://blog.naver.com/rladudwo0908/221233509979
