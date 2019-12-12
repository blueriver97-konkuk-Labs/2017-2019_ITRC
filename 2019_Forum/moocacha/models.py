from django.db import models
from functools import partial

def _wrapper(instance, filename, path):
    ext = filename.split('.')[-1]
    return '{}{}.{}'.format(path, instance.file_name, ext)

def update_filename(path):
    return partial(_wrapper, path=path)


# Create your models here.
class User(models.Model):
    ROLE_LIST = (
        ('1', '학생'),
        ('2', '교수'),
    )
    userId = models.CharField(max_length=20, primary_key=True, verbose_name="아이디")
    password = models.CharField(max_length=10)
    role = models.CharField(max_length=1, choices=ROLE_LIST, verbose_name="역할")
    
    def __str__(self):
        return self.userId

class File(models.Model):
    file_name = models.CharField(max_length=50, verbose_name="최종 파일명(*)") 
    thumbnail = models.ImageField(upload_to=update_filename('thumbnail/'), blank=True, verbose_name="미리보기 이미지")
    video = models.FileField(upload_to=update_filename('video/'), verbose_name="동영상 첨부파일(*)")
    aiml = models.FileField(upload_to=update_filename('aiml/'), blank=True, verbose_name="AIML 첨부파일")

    def __str__(self):
        return self.dst_file_name + ": " + str(self.video)


