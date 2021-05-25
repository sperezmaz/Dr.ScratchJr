from __future__ import unicode_literals

from django.db import models

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
    # data = models.ForeignKey(Data, on_delete=models.CASCADE)
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


class Block_analysis(models.Model):
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
    # average = models.FloatField()


class Bad_habits(models.Model):
    student = models.CharField(max_length=200)
    name_file = models.CharField(max_length=200)
    mtime = models.CharField(max_length=200)
    deadcode = models.CharField(max_length=200)
    unfinishedcode = models.CharField(max_length=200)
    adjacentcode = models.CharField(max_length=200)
    sprites_tot = models.CharField(max_length=200)
    text_sequences = models.CharField(max_length=200, default="")
    num_pages = models.CharField(max_length=200)
    unedited_sprites = models.CharField(max_length=200)
    unedited_pages = models.CharField(max_length=200)
    sprites_in_pages = models.CharField(max_length=200)
    sprites_same_name = models.CharField(max_length=200)
    edited_pages = models.CharField(max_length=200, default="")
    edited_sprites = models.CharField(max_length=200, default="")


class Analysis_types(models.Model):
    variability = models.CharField(max_length=200, default="")
    badhabits = models.CharField(max_length=200, default="")
    otherdata = models.CharField(max_length=200, default="")
    creativity = models.CharField(max_length=200, default="")


class Student(models.Model):
    owner = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __unicode__(self,):
        return self.title


class StudentFiles(models.Model):
    student = models.ForeignKey(Student, related_name='files',
                                on_delete=models.PROTECT)
    file_up = models.FileField(upload_to='web/files/')
    timestamp = models.DateTimeField(auto_now_add=False, auto_now=True)
    mtime = models.CharField(max_length=200)

    def __unicode__(self,):
        return str(self.file_up)


class Files(models.Model):
    file_up = models.FileField(upload_to='web/files/')


class Files_zip(models.Model):
    zip_up = models.FileField(upload_to='web/files_zip/')


class Files_zips(models.Model):
    zip_name = models.CharField(max_length=200, default='')
    student_name = models.CharField(max_length=200)
    student_obj_zip = models.ForeignKey(Student, on_delete=models.PROTECT, default='', null=True)
    file_name = models.CharField(max_length=200)
    project = models.CharField(max_length=200)
    mtime = models.CharField(max_length=200, default='')