from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.safestring import mark_safe
from django.conf import settings
import threading               
import datetime
import json
import os
from .forms import *
from . import gcpapi
# Create your views here.

video_file_path = os.path.join(settings.MEDIA_ROOT, 'video/')
audio_file_path = os.path.join(settings.MEDIA_ROOT, 'audio/')
script_file_path = os.path.join(settings.MEDIA_ROOT, 'script/')
aiml_file_path = os.path.join(settings.MEDIA_ROOT, 'aiml/')
thumb_file_path = os.path.join(settings.MEDIA_ROOT, 'thumbnail/')
BUCKET_NAME = settings.BUCKET_NAME

def genScript(file_name):
    gcpapi.audio_to_script(file_name)
    src_file_path = os.path.join(script_file_path, file_name+'.json')
    dst_file_path = os.path.join('script/', file_name+'.json')
    gcpapi.upload_blob(BUCKET_NAME, src_file_path, dst_file_path)
@csrf_exempt
def index(request):
    return render(request, 'moocacha/index.html')


#@csrf_exempt
#def signup(request):
#    if request.method == 'POST':
#        form = SignUpForm(request.POST)
#        if form.is_valid():
#            #print(form.cleaned_data)
#            if form.cleaned_data['password'] == form.cleaned_data['password_check']:
#                form.save()
#                return redirect('/signin')
#            else:
#                return redirect('/signup')
#    else:
#        form = SignUpForm()
#        return render(request, 'moocacha/signup.html', {'form':form})

#@csrf_exempt
#def signin(request):
#    if request.method == 'POST':
#        form = SignInForm(request.POST)
#        if form.is_valid():
#            user = User.objects.get(userId=form.cleaned_data['userId'])
#            if user.password == form.cleaned_data['password']:
#                return redirect('/')
#            else:
#                return redirect('/signin')
#        else:
#            return redirect('/')
#    else:
#        form = SignInForm()
#        return render(request, 'moocacha/signin.html', {'form':form})

@csrf_exempt
def main(request):
    data = dict()
    blobs = gcpapi.list_blobs_with_prefix('BUCKET_NAME', 'video/')
    video = settings.SAMPLE_VIDEO       

    if 'video' in request.GET.keys():
        video = request.GET['video']

    data['videos'] = list()
    for blob in blobs:
        name = blob.name.split('/')[-1]
        name = name.replace('\'', '')
        
        expiration = datetime.datetime.now()+datetime.timedelta(hours=1)
        if name != '' and name != video:
            meta = dict()
            meta['url'] = blob.generate_signed_url(expiration)
            meta['title'] = name
            data['videos'].append(meta)
        elif name == video:
            data['main_title'] = name
            data['main_url'] = blob.generate_signed_url(expiration)
        else:
            pass

    return render(request, 'moocacha/main.html', data)

@csrf_exempt
def upload(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            file_name = form.cleaned_data['file_name']
#            video_list = gcpapi.list_blobs_with_prefix('BUCKET_NAME', '/video')
#            if file_name in video_list:
#                return render(request, 'moocacha/upload.html', {'form':form, 'ret':-1})
            
            # upload file save to local
            form.save()
            
            # video to audio
            gcpapi.video_to_audio(file_name)

            # upload video to cloud
            src_file_path = os.path.join(video_file_path, file_name+'.mp4')
            dst_file_path = os.path.join('video/', file_name+'.mp4')
            gcpapi.upload_blob('BUCKET_NAME', src_file_path, dst_file_path)
            
            # upload audio to cloud
            src_file_path = os.path.join(audio_file_path, file_name+'.flac')
            dst_file_path = os.path.join('audio/', file_name+'.flac')
            gcpapi.upload_blob('BUCKET_NAME', src_file_path, dst_file_path)

            # make thread
            thread = threading.Thread(target=genScript, args=(file_name,))
            thread.daemon = True
            thread.start()
            
            # audio to script
            #gcpapi.audio_to_script(file_name)

            # upload script to cloud
            #src_file_path = os.path.join(script_file_path, file_name+'.json')
            #dst_file_path = os.path.join('script/', file_name+'.json')
            #gcpapi.upload_blob('BUCKET_NAME', src_file_path, dst_file_path)

            if form.cleaned_data['thumbnail'] is not None:
                pass

            if form.cleaned_data['aiml'] is not None:
                pass

            return redirect('/')
        else:
            return redirect('/')
    else:
        form = UploadForm()
        return render(request, 'moocacha/upload.html', {'form':form})
