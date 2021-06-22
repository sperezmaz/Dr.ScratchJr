from __future__ import unicode_literals

from django.db import models
import random
import string

# Models.


class Data (models.Model):
    ctime = models.CharField(max_length=200, default='2000-01-01 00:00:01')
    mtime = models.CharField(max_length=200)
    name_proyect = models.CharField(max_length=200)
    pagecount = models.IntegerField()
    currentpage = models.CharField(max_length=200)
    version = models.CharField(max_length=200)


class Page (models.Model):
    mtime = models.CharField(max_length=200)
    textstartat = models.FloatField()
    background = models.CharField(max_length=200)
    num_page = models.CharField(max_length=200)


class Sprite (models.Model):
    mtime = models.CharField(max_length=200)
    page = models.CharField(max_length=200)
    shown = models.CharField(max_length=200)
    looks = models.CharField(max_length=200)
    type_sprite = models.CharField(max_length=200)
    id_name = models.CharField(max_length=200)
    flip = models.CharField(max_length=200)
    name_sprite = models.CharField(max_length=200)
    angle = models.FloatField()
    scale = models.FloatField()
    speed = models.FloatField()
    defaultscale = models.FloatField()
    sounds = models.CharField(max_length=200)
    xcoor = models.FloatField()
    ycoor = models.FloatField()
    cx = models.FloatField()
    cy = models.FloatField()
    w = models.FloatField()
    h = models.FloatField()
    homex = models.FloatField()
    homey = models.FloatField()
    homescale = models.FloatField()
    homeshown = models.CharField(max_length=200)
    scripts = models.CharField(max_length=1000)


class Text (models.Model):
    mtime = models.CharField(max_length=200)
    page = models.CharField(max_length=200)
    shown = models.CharField(max_length=200)
    type_sprite = models.CharField(max_length=200)
    id_name = models.CharField(max_length=200)
    speed = models.FloatField()
    cx = models.FloatField()
    cy = models.FloatField()
    w = models.FloatField()
    h = models.FloatField()
    xcoor = models.FloatField()
    ycoor = models.FloatField()
    homex = models.FloatField()
    homey = models.FloatField()
    str_txt = models.CharField(max_length=200)
    color = models.CharField(max_length=200)
    fontsize = models.FloatField()


class Variability(models.Model):
    student = models.CharField(max_length=200)
    name_file = models.CharField(max_length=200)
    mtime = models.CharField(max_length=200)
    triggerings = models.CharField(max_length=200)
    motion = models.CharField(max_length=200)
    looks = models.CharField(max_length=200)
    control = models.CharField(max_length=200)
    sound = models.CharField(max_length=200)
    ends = models.CharField(max_length=200)
    total = models.IntegerField()
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)
    # average = models.FloatField()


class Bad_habits(models.Model):
    student = models.CharField(max_length=200)
    name_file = models.CharField(max_length=200)
    mtime = models.CharField(max_length=200)
    deadcode = models.CharField(max_length=200)
    unfinishedcode = models.CharField(max_length=200)
    adjacentcode = models.CharField(max_length=200)
    sprites_same_name = models.CharField(max_length=200)


class Creativity(models.Model):
    student = models.CharField(max_length=200)
    name_file = models.CharField(max_length=200)
    mtime = models.CharField(max_length=200)
    edited_pages = models.CharField(max_length=600)
    edited_sprites = models.CharField(max_length=600)
    sprites_sound_created = models.CharField(max_length=600)


class Other_data(models.Model):
    student = models.CharField(max_length=200)
    name_file = models.CharField(max_length=200)
    mtime = models.CharField(max_length=200)
    sprites_tot = models.CharField(max_length=200)
    text_sequences = models.CharField(max_length=200)
    pages_tot = models.CharField(max_length=200)
    unedited_sprites = models.CharField(max_length=200)
    unedited_pages = models.CharField(max_length=200)
    sprites_in_pages = models.CharField(max_length=200)


class Analysis_types(models.Model):
    file_name = models.CharField(max_length=200)
    mtime = models.CharField(max_length=200)
    variability = models.CharField(max_length=200)
    badhabits = models.CharField(max_length=200)
    otherdata = models.CharField(max_length=200)
    creativity = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)


class Student(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self,):
        return self.title


def get_path_(min_path):
    letters = string.ascii_letters
    rand_folder = ''.join(random.choice(letters) for _ in range(6))
    folder_upload = min_path + rand_folder
    return folder_upload


class StudentFiles(models.Model):
    student = models.ForeignKey(Student, related_name='files',
                                on_delete=models.PROTECT)
    file_up = models.FileField(upload_to=get_path_('web/files/'))
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)
    mtime = models.CharField(max_length=200)

    def __unicode__(self,):
        return str(self.file_up)


class Files(models.Model):
    file_up = models.FileField(upload_to=get_path_('web/files/'))


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/web/<rand_folder>/<filename>
    return 'web/file_up_zip/{0}/{1}'.format(instance.rand_folder, filename)


class Files_zip(models.Model):
    zip_up = models.FileField(upload_to=user_directory_path)
    rand_folder = models.CharField(max_length=200)


class Files_zips(models.Model):
    zip_name = models.CharField(max_length=200)
    student_name = models.CharField(max_length=200)
    student_obj_zip = models.ForeignKey(Student, on_delete=models.CASCADE,
                                        default='', null=True)
    file_name = models.CharField(max_length=200)
    project = models.CharField(max_length=200)
    mtime = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    rand_folder = models.CharField(max_length=200)


class Contact(models.Model):
    email = models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.email
