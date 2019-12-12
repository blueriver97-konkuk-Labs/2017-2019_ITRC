# ITRC2019-Chatbot

ITRC Forum 2019 - Chatbot Project Git repository

##### Copyright 2019, Embedded Intelligent Computing Laboratory, KonKuk Univ.

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


#### 5. install Packages

    (itrc) $ pip install --upgrade pip
    (itrc) $ pip install django django_extensions channels setuptools google-cloud-speech google-cloud-storage pydub Pillow aiml 
    (itrc) $ apt-get install ffmpeg

    
#### 6. git clone repo

    (itrc) $ git clone git_url
    
#### 7. change directory

    (itrc) $ cd ITRC2019

#### 8. run server
    
    (itrc) $ python3 manage.py runserver 0.0.0.0:8000
    
---------------------------------------
    
##### Git Commit 기본 에디터 변경

    $ git config --global core.editor "vim"
