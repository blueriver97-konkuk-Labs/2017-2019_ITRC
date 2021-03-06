# Generated by Django 2.2.3 on 2019-07-16 11:04

from django.db import migrations, models
import functools
import moocacha.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(max_length=50, verbose_name='최종 파일명(*)')),
                ('thumbnail', models.ImageField(blank=True, upload_to=functools.partial(moocacha.models._wrapper, *(), **{'path': 'thumbnail/'}), verbose_name='미리보기 이미지')),
                ('video', models.FileField(upload_to=functools.partial(moocacha.models._wrapper, *(), **{'path': 'video/'}), verbose_name='동영상 첨부파일(*)')),
                ('aiml', models.FileField(blank=True, upload_to=functools.partial(moocacha.models._wrapper, *(), **{'path': 'aiml/'}), verbose_name='AIML 첨부파일')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.CharField(max_length=20, primary_key=True, serialize=False, verbose_name='아이디')),
                ('password', models.CharField(max_length=10)),
                ('role', models.CharField(choices=[('1', '학생'), ('2', '교수')], max_length=1, verbose_name='역할')),
            ],
        ),
    ]
