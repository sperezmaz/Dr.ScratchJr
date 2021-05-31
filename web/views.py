# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import os
import zipfile
import shutil
import time
import json
import copy
import csv
import random
import string
from datetime import datetime
from django.http import FileResponse
from django.conf import settings
from django.core.mail import send_mail
import pandas as pd
from os import remove
from shutil import rmtree
from django.shortcuts import render
from django.http import HttpResponse
from .models import Data
from .models import Page
from .models import Sprite, Text
from .models import Block_analysis, Bad_habits
from .models import Analysis_types
from .models import Student, StudentFiles
from .models import Files
from .models import Files_zip, Files_zips
from django.contrib.auth.models import User
from django.forms import formset_factory
from .forms import UploadFilesForm, UploadFilesGuestForm, ProfileForm
from .forms import UploadZipForm, FilesForm
from .forms import ContactForm
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist


triggering_blocks = ['onflag', 'onclick', 'ontouch', 'message', 'onmessage']
motion_blocks = ['forward', 'back', 'up', 'down', 'right', 'left', 'hop',
                 'home']
looks_blocks = ['say', 'grow', 'shrink', 'same', 'hide', 'show']
sound_blocks = ['playsnd', 'playusersnd']
control_blocks = ['wait', 'stopmine', 'repeat', 'setspeed']
end_blocks = ['endstack', 'forever', 'gotopage']
blocks_with_atrib = ['forward', 'back', 'up', 'down', 'right', 'left', 'hop',
                     'grow', 'shrink', 'wait', 'repeat']
blocksDict = {'Triggerings': ['onflag', 'onclick', 'ontouch', 'message',
                              'onmessage'],
              'Motion': ['forward-back', 'up-down', 'left-right', 'hop',
                         'home'],
              'Looks': ['say', 'grow-shrink', 'same', 'hide-show'],
              'Sound': ['playsnd', 'playusersnd'],
              'Control': ['wait', 'stopmine', 'repeat', 'setspeed'],
              'Ends': ['endstack', 'forever', 'gotopage'],
              'Total': 23}


def home_view(request):
    """View that builds the template base.html and deletes some stored data."""
    students = []
    remove_old()
    if request.user.is_authenticated:
        student_objs = Student.objects.all()
        for obj in student_objs:
            if Student.objects.filter(owner=request.user).exists():
                if obj.owner == request.user:
                    students.append(str(obj.title))
    form = UploadFilesForm()
    return render(request, "base.html", {'form': form, 'students': students})


def functioning_view(request):
    """View that builds the template functioning.html."""
    return render(request, "functioning.html", {})


def basedatos(request):
    name_student = Analysis_types.objects.all()
    html = "<p>------------------------Listado de Analysis_types: </p>"
    for obj0 in name_student:
        html += '<p>' + str(obj0.file_name) + '<p>'
        html += '<p>' + str(obj0.variability) + '<p>'
        html += '<p>' + str(obj0.badhabits) + '<p>'
        html += '<p>' + str(obj0.otherdata) + '<p>'

    name_student = Student.objects.all()
    html += "<p>------------------------------------Listado de Students: </p>"
    for obj0 in name_student:
        html += '<p>' + str(obj0.owner) + '<p>'
        html += '<p>' + str(obj0.title) + '<p>'
        html += '<p>' + str(obj0.timestamp) + '<p>'
        html += '<p>' + str(obj0.updated) + '<p>'

    name_studentfiles = StudentFiles.objects.all()
    html += "<p>--------------------------------Listado de StudentFiles: </p>"
    for obj in name_studentfiles:
        html += '<p>' + str(obj.student.title) + '<p>'
        html += '<p>' + str(obj.student) + '<p>'
        html += '<p>' + str(obj.file_up) + '<p>'
        html += '<p>' + str(obj.timestamp) + '<p>'
        html += '<p> aaaaaaaaaaaaaamtime: ' + str(obj.mtime) + '<p>'

    block_evalua_obj = Block_analysis.objects.all()
    html += "<p>-----Listado de Block_analysis (student, mtime y name): </p>"
    for obj in block_evalua_obj:
        html += '<p> student: ' + obj.student + '<p>'
        html += '<p> name_file: ' + obj.name_file + '<p>'
        html += '<p> mtime: ' + obj.mtime + '<p>'
        html += '<p> mtime: ' + str(obj.updated) + '<p>'

    # bad_habits_obj = Bad_habits.objects.all()
    # html += "<p>Listado de Bad_habits (student, mtime y name): </p>"
    # for obj3 in bad_habits_obj:
    #     html += '<p> sprites_tot: ' + obj3.sprites_tot + '<p>'
    #     html += '<p> num_pages: ' + obj3.num_pages + '<p>'
    #     html += '<p> unedited_sprites: ' + obj3.unedited_sprites + '<p>'
    #     html += '<p> unedited_pages: ' + obj3.unedited_pages + '<p>'

    name_files = Files_zip.objects.all()
    html += "<p>------------------------------------Listado de Files_zip: </p>"
    for obj2 in name_files:
        html += '<p>' + str(obj2.zip_up) + '<p>'

    name_files = Files_zips.objects.all()
    html += "<p>-----------------------------------Listado de Files_zips: </p>"
    for obj2 in name_files:
        html += '<p>' + str(obj2.zip_name) + '<p>'
        html += '<p>' + str(obj2.student_name) + '<p>'
        html += '<p>student_obj_zip:' + str(obj2.student_obj_zip) + '<p>'
        html += '<p>' + str(obj2.file_name) + '<p>'
        html += '<p>' + str(obj2.project) + '<p>'
        html += '<p>' + str(obj2.timestamp) + '<p>'
        html += '<p>' + str(obj2.rand_folder) + '<p>'
    # name_data = Data.objects.all()
    # html += "<p>-----------------------Listado de Data ( mtime y name): </p>"
    # for obj in name_data:
    #     html += '<p> mtime: ' + obj.mtime + '<p>'

    # name_data = Page.objects.all()
    # html += "<p>-----------------------Listado de Page ( mtime y name): </p>"
    # for obj in name_data:
    #     html += '<p> mtime: ' + obj.mtime + '<p>'

    # name_sprite = Sprite.objects.all()
    # html += "<p>-------------------------------------Listado de Sprite: </p>"
    # for obj in name_sprite:
    #     html += '<p>' + str(obj.mtime) + '<p>'
    #     html += '<p>' + str(obj.scripts) + '<p>'
    return HttpResponse(html)


def contactus_view(request):
    """View that builds the template contactus.html."""
    message = ""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # form.save()
            from_email = form.cleaned_data["email"]
            email_subject = "New contact: " + from_email
            email_subject += ", Subject: " + form.cleaned_data["subject"]
            email_message = form.cleaned_data['message']
            send_mail(email_subject, email_message, from_email,
                      [settings.EMAIL_HOST_USER])
            message = _("Message sent!")
    form = ContactForm()
    return render(request, "contactus.html", {'form': form,
                                              'message': message})


def about_view(request):
    """View that builds the template about.html."""
    return render(request, "about.html", {})


def blocks_view(request):
    """View that builds the template blocks.html."""
    _blocksDict = {}

    for typess in blocksDict:
        if typess == 'Total':
            pass
        else:
            _blocksDict[_(typess)] = blocksDict[typess]
    return render(request, "blocks.html", {'blocksDict': _blocksDict})


def extract_data(files_obj, student_obj):
    """Function extracts zip, opens json.

    Stores the analyzed data if no data exists.

    Then returns the analyzed data.

    """
    name_file = str(files_obj.file_up).split("/")[3]
    folder_file_up = str(files_obj.file_up).split(name_file)[0]
    folder_proj = folder_file_up + 'uncompress_folder'
    # unzip file
    zf = zipfile.ZipFile(str(files_obj.file_up), "r")
    for i in zf.namelist():
        zf.extract(i, folder_proj)
    zf.close()

    # delete uploaded file_up
    if os.path.exists(str(files_obj.file_up)):
        remove(str(files_obj.file_up))

    # copy edited files to characters folder
    if not os.path.exists("web/static/plugins/characters/"):
        os.mkdir('web/static/plugins/characters/')
    try:
        contenidos = os.listdir(folder_proj + '/project/characters')
        for elemento in contenidos:
            shutil.copy2(folder_proj + '/project/characters/' + elemento,
                         'web/static/plugins/characters/')
    except:
        pass

    # extract data from json
    with open(folder_proj + '/project/data.json', encoding="utf8") as file:
        data = json.load(file)
        mtime = data['mtime']

        files_obj.file_up = name_file
        files_obj.save(update_fields=['file_up'])

        if student_obj != "Guest":
            # save json data
            files_obj = save_file(data, files_obj)

        file_name = files_obj.file_up
        name_file = str(file_name).split(".sjr")[0]

        if student_obj == "Guest":
            files_obj.delete()
        try:
            block_analysis = Block_analysis.objects.get(student=student_obj,
                                                        name_file=name_file,
                                                        mtime=mtime)
            block_analysis.save()
        except ObjectDoesNotExist:
            # save data if there isn´t data is stored
            save_data(data)
            analysis(mtime, student_obj, name_file)

        # extracts analyzed data
        (variability_dict, badhabits_dict, otherdat_dict, creativ_dict) = \
            extract_analysis(mtime, student_obj, file_name)

    # delete uploaded folder
    if os.path.exists(folder_file_up):
        shutil.rmtree(folder_file_up)

    return (file_name, mtime, variability_dict, badhabits_dict, otherdat_dict,
            creativ_dict)


def open_projects_in_zip(request, files_obj, path_folder):
    """Function opens json.

    Stores the analyzed data if no data exists.

    """
    # copy edited files to characters folder
    if not os.path.exists("web/static/plugins/characters/"):
        os.mkdir('web/static/plugins/characters/')
    try:
        path_characters = path_folder + '/project/characters'
        contenidos = os.listdir(path_characters)
        for elemento in contenidos:
            shutil.copy2(path_characters + '/' + elemento,
                         'web/static/plugins/characters/')
    except:
        pass

    with open(path_folder + '/project/data.json',
              encoding="utf8") as file:
        data = json.load(file)
        mtime = data['mtime']
        files_obj.mtime = mtime
        files_obj.save(update_fields=['mtime'])
        file_name = files_obj.project + ".sjr"
        # save if user is authenticated
        if request.user.is_authenticated:
            if Student.objects.filter(owner=request.user,
                                      title=files_obj.student_name).exists():
                # authenticated and student name exists
                student_obj = Student.objects.get(owner=request.user,
                                                  title=files_obj.student_name)
                files_obj1 = StudentFiles(student=student_obj,
                                          file_up=file_name)
            else:
                # authenticated and new student name
                student_obj = Student(owner=request.user,
                                      title=files_obj.student_name)
                student_obj.save()
                files_obj1 = StudentFiles(student=student_obj,
                                          file_up=file_name)
            files_obj1.save()
            save_file(data, files_obj1)
            files_obj.student_obj_zip = student_obj
            files_obj.save(update_fields=['student_obj_zip'])
        else:
            student_obj = files_obj.student_name

        try:
            block_analysis = Block_analysis.objects.get(
                                            student=student_obj,
                                            name_file=files_obj.project,
                                            mtime=mtime)
            block_analysis.save()
        except ObjectDoesNotExist:
            # save data if there isn´t data is stored
            save_data(data)
            analysis(mtime, student_obj, files_obj.project)


def create_csv_zip(request, zip_name):
    """Function gets object from the stored zip.

    Creates csv and xlsx files with all the analyzed data of all the projects
     that had the object.

    Returns the csv and xlsx files compressed in a zip file.

    """
    files_obj = Files_zips.objects.filter(zip_name=zip_name)
    letters = string.ascii_letters
    rand_folder = ''.join(random.choice(letters) for _ in range(6))
    folder_upload = "web/csv/" + rand_folder + '/'
    zip = zip_name.split(".zip")[0]
    project_folder = folder_upload + zip
    create_csv(files_obj, zip, folder_upload, project_folder, True)
    response = FileResponse(open(folder_upload + zip + ".zip", 'rb'))
    return response


def create_csv_student(request, student):
    """Function gets object from the stored student.

    Creates csv and xlsx files with all the analyzed data of all the projects
     that had the object.

    Returns the csv and xlsx files compressed in a zip file.

    """
    student_obj = Student.objects.get(owner=request.user, title=student)
    files_obj = StudentFiles.objects.filter(student=student_obj)
    letters = string.ascii_letters
    rand_folder = ''.join(random.choice(letters) for _ in range(6))
    folder_upload = "web/csv/" + rand_folder + '/'
    project_folder = folder_upload + student
    create_csv(files_obj, student, folder_upload, project_folder, False)
    response = FileResponse(open(folder_upload + student + ".zip", 'rb'))
    return response


def create_csv_user(request):
    """Function gets object from the stored user.

    Creates csv and xlsx files with all the analyzed data of all the projects
     that had the object.

    Returns the csv and xlsx files compressed in a zip file.

    """
    files_obj = []
    students_obj = Student.objects.filter(owner=request.user)
    user = str(request.user)
    letters = string.ascii_letters
    rand_folder = ''.join(random.choice(letters) for _ in range(6))
    folder_upload = "web/csv/" + rand_folder + '/'
    project_folder = folder_upload + user
    bad_habits_dict = {}
    os.makedirs(project_folder, exist_ok=True)
    variability_path = project_folder + "/variability-%s.csv"
    variability_path = next_path(variability_path)
    bad_habits_path = project_folder + "/badhabits-%s.csv"
    bad_habits_path = next_path(bad_habits_path)
    other_data_path = project_folder + "/otherdata-%s.csv"
    other_data_path = next_path(other_data_path)
    for student_obj in students_obj:
        files_obj = StudentFiles.objects.filter(student=student_obj)
        for file_obj in files_obj:
            student = file_obj.student
            stud_name = file_obj.student.title
            file_name = file_obj.file_up

            (variability_dict, badhabits_dict, otherdat_dict, creativ_dict) = \
                extract_analysis(file_obj.mtime, student, file_name)

            variability_dict[_('Name')] = stud_name
            variability_dict[_('Project name')] = file_name
            variability_csv(variability_dict, variability_path)

            bad_habits_dict[_('Name')] = stud_name
            bad_habits_dict[_('Project name')] = file_name
            bad_habits_csv(badhabits_dict, bad_habits_dict, bad_habits_path)

            otherdat_dict[_('Name')] = stud_name
            otherdat_dict[_('Project name')] = file_name
            other_data_csv(otherdat_dict, other_data_path)

    variability = pd.read_csv(variability_path, encoding='utf-8')
    bad_habits = pd.read_csv(bad_habits_path, encoding='utf-8')
    other_data = pd.read_csv(other_data_path, encoding='utf-8')
    writer = pd.ExcelWriter(project_folder + "/data.xlsx")
    variability.to_excel(writer, sheet_name=_("Variability"), index=False)
    bad_habits.to_excel(writer, sheet_name=_("Bad_habits"), index=False)
    other_data.to_excel(writer, sheet_name=_("Other_data"), index=False)
    writer.save()

    shutil.copy2("web/csv/README.txt", folder_upload + user)

    # delete zips old (30 min)
    delete_filesbytime("web/csv", 1/48)

    fantasy_zip = zipfile.ZipFile(folder_upload + user + ".zip", 'w')

    for folder, subfolders, files in os.walk(project_folder):
        for file in files:
            fantasy_zip.write(os.path.join(folder, file),
                              os.path.relpath(os.path.join(folder, file),
                                              project_folder),
                              compress_type=zipfile.ZIP_DEFLATED)
    writer.close()

    # delete folder
    if os.path.exists(folder_upload + user):
        shutil.rmtree(folder_upload + user)

    response = FileResponse(open(folder_upload + user + ".zip", 'rb'))
    return response


def create_csv(files_obj, name_zip, folder_upload, project_folder, is_zip):
    """Function.

    Creates csv and xlsx files with all the analyzed data (variability,
     badhabits and otherdata) of all the projects that had the
     object (files_obj).

    """
    bad_habits_dict = {}
    os.makedirs(project_folder, exist_ok=True)
    variability_path = project_folder + "/variability-%s.csv"
    variability_path = next_path(variability_path)
    bad_habits_path = project_folder + "/badhabits-%s.csv"
    bad_habits_path = next_path(bad_habits_path)
    other_data_path = project_folder + "/otherdata-%s.csv"
    other_data_path = next_path(other_data_path)
    for file_obj in files_obj:
        if is_zip:
            if file_obj.student_obj_zip is not None:
                stud_name = file_obj.student_obj_zip.title
                student = file_obj.student_obj_zip
            else:
                stud_name = file_obj.student_name
                student = stud_name
            file_name = file_obj.project
        else:
            student = file_obj.student
            stud_name = file_obj.student.title
            file_name = file_obj.file_up

        (variability_dict, badhabits_dict, otherdat_dict, creativ_dict) = \
            extract_analysis(file_obj.mtime, student, file_name)

        variability_dict[_('Name')] = stud_name
        variability_dict[_('Project name')] = file_name
        variability_csv(variability_dict, variability_path)

        bad_habits_dict[_('Name')] = stud_name
        bad_habits_dict[_('Project name')] = file_name
        bad_habits_csv(badhabits_dict, bad_habits_dict, bad_habits_path)

        otherdat_dict[_('Name')] = stud_name
        otherdat_dict[_('Project name')] = file_name
        other_data_csv(otherdat_dict, other_data_path)

    variability = pd.read_csv(variability_path)
    bad_habits = pd.read_csv(bad_habits_path)
    other_data = pd.read_csv(other_data_path)
    writer = pd.ExcelWriter(project_folder + "/data.xlsx")
    variability.to_excel(writer, sheet_name=_("Variability"), index=False)
    bad_habits.to_excel(writer, sheet_name=_("Bad_habits"), index=False)
    other_data.to_excel(writer, sheet_name=_("Other_data"), index=False)
    writer.save()

    shutil.copy2("web/csv/README.txt", folder_upload + name_zip)

    # delete zips old (30 min)
    delete_filesbytime("web/csv", 1/48)

    fantasy_zip = zipfile.ZipFile(folder_upload + name_zip + ".zip", 'w')

    for folder, subfolders, files in os.walk(project_folder):
        for file in files:
            fantasy_zip.write(os.path.join(folder, file),
                              os.path.relpath(os.path.join(folder, file),
                                              project_folder),
                              compress_type=zipfile.ZIP_DEFLATED)
    writer.close()
    # delete folder
    if os.path.exists(folder_upload + name_zip):
        shutil.rmtree(folder_upload + name_zip)


def write_csv(path, fieldnames, row_dict):
    """Function write csv file."""
    write_header = True
    if os.path.exists(path):
        write_header = False
    else:
        write_header = True

    with open(path, 'a', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerows([row_dict])


def variability_csv(variability_dict, variability_path):
    """Function adapts variability_dict to create csv file."""
    _blocksDict = {}

    for typess in blocksDict:
        _blocksDict[_(typess)] = blocksDict[typess]

    for clave in variability_dict:
        for clave2 in _blocksDict:
            if clave == clave2:
                if clave == 'Average score':
                    pass
                elif clave == 'Total':
                    variability_dict[clave] = str(variability_dict[clave]) + \
                                              "/" + str(_blocksDict[clave2])
                else:
                    len_variab = str(len(variability_dict[clave]))
                    len_blocks = str(len(_blocksDict[clave2]))
                    variability_dict[clave] = len_variab + "/" + len_blocks

    fieldnames = [_('Name'), _('Project name'), _('Triggerings'), _('Motion'),
                  _('Looks'), _('Control'), _('Sound'), _('Ends'), 'Total']

    write_csv(variability_path, fieldnames, variability_dict)


def bad_habits_csv(badhabits_dict, bad_habits_dict, bad_habits_path):
    """Function adapts badhabits_dict to create csv file."""
    fieldnames = [_('Name'), _('Project name'), _('Existence bad habit'),
                  _('Type of bad habit'), _('Page'), _('Character'),
                  _('Sequence name'), _('Sequence')]
    for clave in badhabits_dict:
        bad_habits_dict[_("Type of bad habit")] = clave
        if badhabits_dict[clave] == []:
            bad_habits_dict[_("Existence bad habit")] = _("NONE")
            bad_habits_dict[_("Page")] = "----"
            bad_habits_dict[_("Character")] = "----"
            bad_habits_dict[_("Sequence name")] = "----"
            bad_habits_dict[_("Sequence")] = "----"
            write_csv(bad_habits_path, fieldnames, bad_habits_dict)
        for elem in badhabits_dict[clave]:
            bad_habits_dict[_("Existence bad habit")] = _("YES")
            bad_habits_dict[_("Page")] = elem[0]
            bad_habits_dict[_("Character")] = elem[1]
            bad_habits_dict[_("Sequence name")] = elem[2]
            bad_habits_dict[_("Sequence")] = elem[3]
            write_csv(bad_habits_path, fieldnames, bad_habits_dict)


def other_data_csv(otherdat_dict, other_data_path):
    """Function adapts otherdat_dict to create csv file."""
    fieldnames = [_('Name'), _('Project name'), _('Total pages'), _('Pages'),
                  _('Total sprites'), _('Sprites'), _("Total texts"),
                  _("Texts in pages"),
                  _('Total pages with unedited background'),
                  _('Pages with unedited background'),
                  _('Total unedited sprites'), _('Unedited sprites'),
                  _('Sprites in pages'), _('Sprites same name')]

    otherdat_dict[_("Pages")] = str(otherdat_dict[_("Total pages")])
    otherdat_dict[_("Total pages")] = len(otherdat_dict[_("Total pages")])
    otherdat_dict[_("Sprites")] = str(otherdat_dict[_("Total sprites")])
    otherdat_dict[_("Total sprites")] = len(otherdat_dict[_("Total sprites")])
    otherdat_dict[_("Texts in pages")] = str(otherdat_dict[_("Total texts")])
    otherdat_dict[_("Total texts")] = len(otherdat_dict[_("Total texts")])
    otherdat_dict[_("Total pages with unedited background")] = \
        len(otherdat_dict[_("Pages with unedited background")])
    otherdat_dict[_("Total unedited sprites")] = \
        len(otherdat_dict[_("Unedited sprites")])
    write_csv(other_data_path, fieldnames, otherdat_dict)


def next_path(path_pattern):
    """Function.

    Finds the next free path in an sequentially named list of files.

    Runs in log(n) time where n is the number of existing files in sequence
    """
    i = 1
    # First do an exponential search
    while os.path.exists(path_pattern % i):
        i = i * 2
    # Result lies somewhere in the interval (i/2..i]
    # We call this interval (a..b] and narrow it down until a + 1 = b
    a, b = (i / 2, i)
    while a + 1 < b:
        c = (a + b) / 2  # interval midpoint
        a, b = (c, b) if os.path.exists(path_pattern % c) else (a, c)
    return path_pattern % b


def save_file(data, stdnt_files_obj):
    """Function renames repeated files and saves file data with the student."""
    studentDict = []
    mtime = data['mtime']
    name_studentfiles = StudentFiles.objects.all()
    for obj in name_studentfiles:
        named = False
        if obj.student == stdnt_files_obj.student:
            student_files = str(obj.file_up)
            i = 0
            while not named:
                if student_files in studentDict:
                    i += 1
                    if (not (student_files + " (" + str(i) + ")") in
                            studentDict):
                        student_files = student_files + " (" + str(i) + ")"
                else:
                    named = True
            studentDict.append(student_files)
            if (obj.timestamp == stdnt_files_obj.timestamp and
                    str(obj.file_up) == str(stdnt_files_obj.file_up)):
                stdnt_files_obj.file_up = student_files
                stdnt_files_obj.mtime = mtime
                stdnt_files_obj.save(update_fields=['file_up', 'mtime'])
    return stdnt_files_obj


def save_data(data):
    """Function saves json data in DB (Data, Page, Sprite and Text)."""
    ctime = data['ctime']
    mtime = data['mtime']
    name_proyect = data['name']
    pages = data['json']['pages']
    pagecount = data['thumbnail']['pagecount']
    version = data['version']
    currentpage = data['json']['currentPage']

    archivo = Data(ctime=ctime, mtime=mtime, name_proyect=name_proyect,
                   pagecount=pagecount, currentpage=currentpage,
                   version=version)
    archivo.save()

    for page in pages:
        data_pag = data['json'][page]
        textstartat = data_pag['textstartat']
        try:
            background = data_pag['md5']
        except:
            background = ""
        num_page = int(data_pag['num'])
        page_order = "Pos " + str(num_page) + "-" + page
        info_pag = Page(mtime=mtime, textstartat=textstartat,
                        background=background, num_page=page_order)
        info_pag.save()

        sprites = []
        for sprite_name in data_pag['sprites']:
            sprites.append(sprite_name)
        for i in range(0, len(sprites)):
            features = data_pag[sprites[i]]
            if 'Text' in sprites[i]:
                t = Text(mtime=mtime, page=page_order, shown=features['shown'],
                         type_sprite=features['type'], id_name=features['id'],
                         speed=features['speed'], cx=features['cx'],
                         cy=features['cy'], w=features['w'], h=features['h'],
                         xcoor=features['xcoor'], ycoor=features['ycoor'],
                         homex=features['homex'], homey=features['homey'],
                         str_txt=features['str'], color=features['color'],
                         fontsize=features['fontsize'])
                t.save()
            else:
                p = Sprite(mtime=mtime, page=page_order,
                           shown=features['shown'],
                           type_sprite=features['type'],
                           looks=features['md5'], id_name=features['id'],
                           flip=features['flip'], name_sprite=features['name'],
                           angle=features['angle'], scale=features['scale'],
                           speed=features['speed'],
                           defaultscale=features['defaultScale'],
                           sounds=features['sounds'], xcoor=features['xcoor'],
                           ycoor=features['ycoor'], cx=features['cx'],
                           cy=features['cy'], w=features['w'],
                           h=features['h'], homex=features['homex'],
                           homey=features['homey'],
                           homescale=features['homescale'],
                           homeshown=features['homeshown'],
                           scripts=str(features['scripts']))
                p.save()


def extract_analysis(mtime, student_obj, name_file):
    """Function extracts the analysis data from the DB.

    Returns the dictionaries (variability_dict, badhabits_dict, otherdat_dict,
     creativ_dict) of the analysis.

    """
    name_file = str(name_file).split(".sjr")[0]

    block_analy_obj = Block_analysis.objects.get(student=student_obj,
                                                 name_file=name_file,
                                                 mtime=mtime)
    badhabits_obj = Bad_habits.objects.get(student=student_obj, mtime=mtime,
                                           name_file=name_file)
    variability_dict = {}
    badhabits_dict = {}
    otherdat_dict = {}
    creativ_dict = {}

    variability_dict[_("Triggerings")] = eval(block_analy_obj.triggerings)
    variability_dict[_("Motion")] = eval(block_analy_obj.motion)
    variability_dict[_("Looks")] = eval(block_analy_obj.looks)
    variability_dict[_("Control")] = eval(block_analy_obj.control)
    variability_dict[_("Sound")] = eval(block_analy_obj.sound)
    variability_dict[_("Ends")] = eval(block_analy_obj.ends)

    variability_dict["Total"] = block_analy_obj.total

    badhabits_dict[_("Dead code")] = eval(badhabits_obj.deadcode)
    badhabits_dict[_("Unfinished code")] = eval(badhabits_obj.unfinishedcode)
    badhabits_dict[_("Sequences with adjacent blocks")] = \
        eval(badhabits_obj.adjacentcode)

    otherdat_dict[_("Total pages")] = eval(badhabits_obj.num_pages)
    otherdat_dict[_("Total sprites")] = eval(badhabits_obj.sprites_tot)
    otherdat_dict[_("Total texts")] = eval(badhabits_obj.text_sequences)
    otherdat_dict[_("Pages with unedited background")] = \
        eval(badhabits_obj.unedited_pages)
    otherdat_dict[_("Unedited sprites")] = eval(badhabits_obj.unedited_sprites)
    otherdat_dict[_("Sprites in pages")] = eval(badhabits_obj.sprites_in_pages)
    otherdat_dict[_("Sprites same name")] = \
        eval(badhabits_obj.sprites_same_name)

    creativ_dict[_("Edited pages")] = eval(badhabits_obj.edited_pages)
    creativ_dict[_("Edited sprites")] = eval(badhabits_obj.edited_sprites)

    if student_obj == "Guest":
        block_analy_obj.delete()
        badhabits_obj.delete()

    return variability_dict, badhabits_dict, otherdat_dict, creativ_dict


def upload_files_view(request):
    """View that builds the template upload.html.

    If the form is valid:
        Stores in DB the project received from a form and extracts data from
         that project and stores it in DB.

        Deletes folders that were created in the process.

    """
    form = UploadFilesGuestForm()
    message = ""
    name = ""
    students = []
    variability_d = {}
    badhabits_d = {}
    otherdat_d = {}
    creativ_d = {}
    _blocksDict = {}

    for typess in blocksDict:
        _blocksDict[_(typess)] = blocksDict[typess]

    def choose_forms():
        """Function determines type of form if you are logged in or not."""
        if request.user.is_authenticated:
            student_objs = Student.objects.all()
            for obj in student_objs:
                if Student.objects.filter(owner=request.user).exists():
                    if obj.owner == request.user:
                        students.append(str(obj.title))
            form = UploadFilesForm()
        else:
            form = UploadFilesGuestForm()

    if request.method == 'POST':
        if request.user.is_authenticated:
            form = UploadFilesForm(request.POST, request.FILES)
        else:
            form = UploadFilesGuestForm(request.POST, request.FILES)

        if form.is_valid():
            remove_old()
            try:
                name_student = form.cleaned_data['name_student'].title()
                if name_student == "Guest":
                    message = 'The name "Guest" is reserved for guests!'
                    choose_forms()
            except:
                name_student = "Guest"

            if (str(request.FILES['file']).find(".sjr") != -1 and
                    message != 'The name "Guest" is reserved for guests!'):
                file_up = request.FILES['file']

                if not request.user.is_authenticated:
                    # if not authenticated only save file
                    files_obj = Files(file_up=file_up)
                    student_obj = name_student
                elif Student.objects.filter(owner=request.user,
                                            title=name_student).exists():
                    # authenticated and student name exists
                    student_obj = Student.objects.get(owner=request.user,
                                                      title=name_student)
                    files_obj = StudentFiles(student=student_obj,
                                             file_up=file_up)
                else:
                    # authenticated and new student name
                    student_obj = Student(owner=request.user,
                                          title=name_student)
                    student_obj.save()
                    files_obj = StudentFiles(student=student_obj,
                                             file_up=file_up)
                files_obj.save()
                message = _("File uploaded succesfully!")

                # extract data from uploaded file
                (name, mtime, variability_d, badhabits_d, otherdat_d,
                 creativ_d) = extract_data(files_obj, student_obj)

                save_analys(str(name), mtime, variability_d, badhabits_d,
                            otherdat_d, creativ_d)

                # delete edited images after 1 year
                delete_filesbytime('web/static/plugins/characters/', 365)

            elif str(request.FILES['file']).find(".sjr") == -1:
                message = _("The file must have the extension .sjr!")
                choose_forms()
        else:
            message = _("Fill the required fields")
            choose_forms()
    else:
        choose_forms()
    return render(request, 'upload.html', {'form': form, 'message': message,
                                           'file_up': name, 'mtime': mtime,
                                           'students': students,
                                           'variability_dict': variability_d,
                                           'badhabits_dict': badhabits_d,
                                           'otherdat_dict': otherdat_d,
                                           'creativ_dict': creativ_d,
                                           'blocksDict': _blocksDict})


def upload_file_zip_view(request):
    """View that builds the template up_zip.html .

    1º If the form is valid:
        Extracts the projects from the uploaded zip and retrieves their names
         to generate the formset.
    2º If the formset is valid:
        Stores in DB the projects received from a formset and extracts data
         from these projects and stores it in DB.

        Deletes folders that were created in the process.

    """
    form = UploadZipForm()
    message = ""
    inicial_form = []
    elementos = []
    FileFormSet = formset_factory(FilesForm, extra=0)

    if request.method == 'POST':
        form = UploadZipForm(request.POST, request.FILES)
        formset = FileFormSet(request.POST)
        if form.is_valid():
            remove_old()
            if str(request.FILES['file']).find(".zip") != -1:

                message = _("File uploaded succesfully!")
                file_up = request.FILES['file']
                letters = string.ascii_letters
                rand_folder = ''.join(random.choice(letters) for _ in range(6))
                filezip_obj = Files_zip(zip_up=file_up,
                                        rand_folder=rand_folder)
                filezip_obj.save()

                name_file = str(filezip_obj.zip_up).split("/")[3]
                unzip_folder = str(filezip_obj.zip_up).split(name_file)[0]

                zipf = zipfile.ZipFile(str(filezip_obj.zip_up), "r")
                for i in zipf.namelist():
                    zipf.extract(i, unzip_folder + 'proj')
                zipf.close()

                # delete uploaded file zip and obj Files_zip
                if os.path.exists(str(filezip_obj.zip_up)):
                    remove(str(filezip_obj.zip_up))
                    filezip_obj.delete()
                try:
                    contenidos = os.listdir(unzip_folder + 'proj')
                    for elemento in contenidos:
                        elemento = str(elemento)
                        project = elemento.split("-")[0]
                        student = elemento.split("-")[1]
                        student = student.split(".sjr")[0]
                        proyects = {}
                        proyects['student'] = str(student)
                        proyects['project'] = str(project)
                        proyects['unzip_folder'] = unzip_folder
                        inicial_form.append(proyects)
                        elementos.append(elemento)
                        files_obj = Files_zips(zip_name=file_up,
                                               student_name=str(student),
                                               file_name=elemento,
                                               project=str(project),
                                               rand_folder=rand_folder)
                        files_obj.save()
                except:
                    message = "Projects must be named as indicated in the form"
                    message += " description"
                    message = _(message)
                    form = UploadZipForm()
                    return render(request, 'up_zip.html', {'form': form,
                                                           'message': message})
                formset = FileFormSet(initial=inicial_form)
                return render(request, 'up_zip.html', {'formset': formset,
                                                       'message': message,
                                                       'elementos': elementos})

            elif str(request.FILES['file']).find(".zip") == -1:
                message = _("The file must have the extension .zip!")
        elif not form.is_valid():
            # try:
            if formset.is_valid():
                n = 0
                for f in formset:
                    # update data with formset
                    unzip_folder = f.cleaned_data['unzip_folder']
                    rand_folder = unzip_folder.split('/')[-2]
                    contenidos = os.listdir(unzip_folder + 'proj')
                    name = str(contenidos[n])
                    files_obj = Files_zips.objects.get(file_name=name,
                                                       rand_folder=rand_folder)
                    stud_name = f.cleaned_data['student'].title()
                    files_obj.student_name = stud_name
                    files_obj.project = f.cleaned_data['project']
                    files_obj.save(update_fields=['student_name', 'project'])

                    proyects = {}
                    proyects[str(files_obj.student_name)] = \
                        [str(files_obj.project), str(files_obj.file_name)]
                    inicial_form.append(proyects)

                    # extract projects
                    path_files = unzip_folder + 'proj/' + contenidos[n]
                    zf = zipfile.ZipFile(path_files, "r")
                    folder = str(contenidos[n].split(".sjr")[0])
                    path_folder = unzip_folder + 'projs/' + folder
                    for i in zf.namelist():
                        zf.extract(i, path_folder)
                    n += 1
                    open_projects_in_zip(request, files_obj, path_folder)

                zf.close()
                # delete uploaded folder
                if os.path.exists(unzip_folder):
                    shutil.rmtree(unzip_folder)

                return render(request, 'review_zip.html',
                              {'zip_name': files_obj.zip_name,
                               'inicial_form': inicial_form,
                               'rand_folder': rand_folder,
                               'message': message})
            # except:
            #     pass
            message = _("Fill the required fields")
            form = UploadZipForm()
    else:
        form = UploadZipForm()
    return render(request, 'up_zip.html', {'form': form, 'message': message})


def remove_old():
    """Function removes objects from the DB that are no longer needed."""
    utc_now = datetime.utcnow()
    utc_now = str(utc_now).split(".")[0]
    utc_now_sec = datetime.strptime(utc_now, '%Y-%m-%d %H:%M:%S')
    utc_now_sec = time.mktime(utc_now_sec.timetuple())

    # delete objs after 2h
    seconds = utc_now_sec - 7200

    def get_time(timestamp):
        """Function converts date to seconds."""
        time_date = str(timestamp)
        time_date = time_date.split(".")[0]
        dt = datetime.strptime(time_date, '%Y-%m-%d %H:%M:%S')
        ts = time.mktime(dt.timetuple())
        return ts

    fileszip_objs_all = Files_zips.objects.all()
    for fileszip_objs in fileszip_objs_all:
        time_file = get_time(fileszip_objs.timestamp)
        if seconds >= time_file:
            if fileszip_objs.student_obj_zip is None:
                try:
                    block_analy_obj = Block_analysis.objects.get(
                                            student=fileszip_objs.student_name,
                                            mtime=fileszip_objs.mtime,
                                            name_file=fileszip_objs.project)
                    badhabits_obj = Bad_habits.objects.get(
                                            student=fileszip_objs.student_name,
                                            mtime=fileszip_objs.mtime,
                                            name_file=fileszip_objs.project)

                    time_obj = get_time(block_analy_obj.updated)
                    if seconds >= time_obj:
                        block_analy_obj.delete()
                        badhabits_obj.delete()
                        fileszip_objs.delete()
                except:
                    fileszip_objs.delete()
            else:
                fileszip_objs.delete()

    analysis_types_objs = Analysis_types.objects.all()
    for analysis_types in analysis_types_objs:
        sec_analysis = get_time(analysis_types.timestamp)
        # delete objs after 30 min
        seconds_anal = utc_now_sec - 1800
        if seconds_anal >= sec_analysis:
            analysis_types.delete()


def save_analys(file_name, mtime, varia_d, badhabits_d, otherdat_d, creativ_d):
    """Function.

    Removes the dictionaries from the analysis of an old project from the
     DB and stores the new dictionaries that it receives.

    """
    try:
        analys_obj = Analysis_types.objects.get(file_name=file_name,
                                                mtime=mtime)
        analys_obj.delete()
    except ObjectDoesNotExist:
        pass
    analys_obj = Analysis_types(file_name=file_name, mtime=mtime,
                                variability=varia_d, badhabits=badhabits_d,
                                otherdata=otherdat_d, creativity=creativ_d)
    analys_obj.save()


def analysis_view(request, name, name_file):
    """View that builds the template analysis.html.

    Extracts analysis and saves it in the DB.

    """
    _blocksDict = {}
    student_obj = Student.objects.get(owner=request.user, title=name)
    file_objs = StudentFiles.objects.get(student=student_obj,
                                         file_up=name_file)

    (variab_dict, badhabit_dict, otherdat_dict, creativ_dict) = \
        extract_analysis(file_objs.mtime, student_obj, name_file)

    save_analys(str(file_objs.file_up), file_objs.mtime, variab_dict,
                badhabit_dict, otherdat_dict, creativ_dict)

    for typess in blocksDict:
        _blocksDict[_(typess)] = blocksDict[typess]

    return render(request, "analysis.html", {'file_up': file_objs.file_up,
                                             'mtime': file_objs.mtime,
                                             'variability_dict': variab_dict,
                                             'badhabits_dict': badhabit_dict,
                                             'otherdat_dict': otherdat_dict,
                                             'creativ_dict': creativ_dict,
                                             'blocksDict': _blocksDict})


def analysis2_view(request, name, project, file_name, rand_folder):
    """View that builds the template analysis.html.

    Extracts analysis and saves it in the DB.

    """
    _blocksDict = {}
    if request.user.is_authenticated:
        student_obj = Student.objects.get(owner=request.user, title=name)
        files_obj = Files_zips.objects.get(rand_folder=rand_folder,
                                           file_name=file_name,
                                           student_obj_zip=student_obj,
                                           student_name=name, project=project)
        student = files_obj.student_obj_zip
    else:
        files_obj = Files_zips.objects.get(rand_folder=rand_folder,
                                           file_name=file_name,
                                           student_name=name, project=project,
                                           student_obj_zip__isnull=True)
        student = files_obj.student_name

    (variab_dict, badhabit_dict, otherdat_dict, creativ_dict) = \
        extract_analysis(files_obj.mtime, student, files_obj.project)

    save_analys(files_obj.file_name, files_obj.mtime, variab_dict,
                badhabit_dict, otherdat_dict, creativ_dict)

    for typess in blocksDict:
        _blocksDict[_(typess)] = blocksDict[typess]

    return render(request, "analysis.html", {'file_up': files_obj.file_name,
                                             'mtime': files_obj.mtime,
                                             'variability_dict': variab_dict,
                                             'badhabits_dict': badhabit_dict,
                                             'otherdat_dict': otherdat_dict,
                                             'creativ_dict': creativ_dict,
                                             'blocksDict': _blocksDict})


def results_view(request, file_name, mtime, type1, type2):
    """View that builds the template results.html.

    Adapts the saved analyses of a project in lists for the template.

    """
    _blocksDict = {}
    unused_blocks = []
    bad_habits = []
    other_data = []
    creativity = []

    analys_obj = Analysis_types.objects.get(file_name=file_name, mtime=mtime)

    for typess in blocksDict:
        _blocksDict[_(typess)] = blocksDict[typess]

    unused_blocksDict = copy.deepcopy(_blocksDict)

    if type1 == 'badhabits':
        dict_obj = eval(analys_obj.badhabits)
        for elem in dict_obj:
            if elem == type2:
                bad_habits = dict_obj[elem]
    elif type1 == 'variability':
        dict_obj = eval(analys_obj.variability)
        for elem in dict_obj:
            if elem == type2:
                blocks = dict_obj[elem]
                unused_blocks = unused_blocksDict[elem]
                for block in blocks:
                    if block in _blocksDict[elem]:
                        unused_blocksDict[elem].remove(block)
                        unused_blocks = unused_blocksDict[elem]
    elif type1 == 'creativity':
        dict_obj = eval(analys_obj.creativity)
        for elem in dict_obj:
            if elem == type2:
                creativity = dict_obj[elem]
    elif type1 == 'otherdata':
        dict_obj = eval(analys_obj.otherdata)
        for elem in dict_obj:
            if elem == type2:
                other_data = dict_obj[elem]
    return render(request, "results.html", {'unused_blocks': unused_blocks,
                                            'bad_habits': bad_habits,
                                            'creativity': creativity,
                                            'other_data': other_data,
                                            'types': type2})


@login_required
def profile_view(request):
    """View that builds the template profile.html."""
    message = ""
    student_objs = Student.objects.filter(owner=request.user)
    students = str(len(student_objs))
    profile_user = User.objects.get(username=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST)
        if form.is_valid():
            profile_user.first_name = form.cleaned_data['first_name']
            profile_user.last_name = form.cleaned_data['surname']
            profile_user.save()
            message = _("Updated data!")
        else:
            message = _("Fill all data!")
            form = ProfileForm()
    else:
        form = ProfileForm()
    return render(request, 'profile.html', {'form': form, 'user': profile_user,
                                            'message': message,
                                            'students': students})


def settings_view(request):
    """View that builds the template settings.html."""
    return render(request, "settings.html", {})


def review_view(request):
    """View that builds the template review.html."""
    students = students_review_dict(request)
    return render(request, "review.html", {'students': students})


def students_review_dict(request):
    """Function returns a dictionary with the students and their projects."""
    students = {}
    student_objs = Student.objects.filter(owner=request.user)
    for student_obj in student_objs:
        students[str(student_obj.title)] = []
        file_objects = StudentFiles.objects.filter(student=student_obj)
        for file_obj in file_objects:
            if file_obj.student.title == student_obj.title:
                students[str(student_obj.title)].append(str(file_obj.file_up))
    return students


def student_view(request, student):
    """View that builds the template student.html."""
    studentDict = student_dict(request, student)
    return render(request, "student.html", {'student': student,
                                            'studentDict': studentDict})


def student_dict(request, name):
    """Function.

    Returns a dictionary with the date, variability and sum of bad habits of a
     student's projects.

    """
    studentDict = {}
    student_obj = Student.objects.get(owner=request.user, title=name)
    file_objects = StudentFiles.objects.filter(student=student_obj)
    for file_obj in file_objects:
        timestamp1 = str(file_obj.timestamp)
        timestamp1 = str(timestamp1.split(".")[0])
        file_up = str(file_obj.file_up)
        name_file = str(file_up).split(".sjr")[0]
        mtime = str(file_obj.mtime)

        block_analy_obj = Block_analysis.objects.get(student=student_obj,
                                                     name_file=name_file,
                                                     mtime=mtime)
        bad_habits_obj = Bad_habits.objects.get(student=student_obj,
                                                name_file=name_file,
                                                mtime=mtime)
        total = str(block_analy_obj.total) + '/' + str(blocksDict['Total'])
        num_bad_habits = 0
        num_bad_habits = len(eval(bad_habits_obj.deadcode))
        num_bad_habits += len(eval(bad_habits_obj.unfinishedcode))
        num_bad_habits += len(eval(bad_habits_obj.adjacentcode))
        studentDict.update({file_up: [timestamp1, total, num_bad_habits]})
    sortedDict = sorted(studentDict.items(), key=lambda x: x[1], reverse=True)
    studentDict = dict(sortedDict)
    return studentDict


def delete_regist(request, student, file_name, times):
    """View that builds the template student.html.

    Removes a project.

    """
    student_obj = Student.objects.get(owner=request.user, title=student)
    delete_file = StudentFiles.objects.get(student=student_obj,
                                           timestamp__icontains=times,
                                           file_up=file_name)
    delete_file.delete()
    message = _("File delete succesfully!")
    studentDict = student_dict(request, student)
    return render(request, "student.html", {'student': student,
                                            'studentDict': studentDict,
                                            'message': message})


def delete_student(request, student):
    """View that builds the template review.html.

    Removes a student.

    """
    student_obj = Student.objects.get(owner=request.user, title=student)
    delete_files_student = StudentFiles.objects.filter(student=student_obj)
    delete_files_student.delete()
    student_obj.delete()
    message = "Student delete succesfully!"
    students = students_review_dict(request)
    return render(request, "review.html", {'students': students,
                                           'message': message})


def edit_student(request, old_student, new_student):
    """View that builds the template review.html.

    Edits a student.

    """
    if Student.objects.filter(owner=request.user, title=new_student).exists():
        message = _("Error: Student's name is already used!")
    else:
        student_obj = Student.objects.get(owner=request.user,
                                          title=old_student)
        student_obj.title = new_student
        student_obj.save(update_fields=['title'])
        message = _("Student edit succesfully!")

    students = students_review_dict(request)
    return render(request, "review.html", {'students': students,
                                           'message': message})


def edit_file(request, old_file, student, new_file):
    """View that builds the template student.html.

    Edits a project.

    """
    student_obj = Student.objects.get(owner=request.user, title=student)
    if StudentFiles.objects.filter(student=student_obj,
                                   file_up=new_file).exists():
        message = _("Error: The file name is already in use!")
    else:
        file_obj = StudentFiles.objects.get(student=student_obj,
                                            file_up=old_file)
        file_obj.file_up = new_file
        file_obj.save(update_fields=['file_up'])
        message = _("File edit succesfully!")
    studentDict = student_dict(request, student)
    return render(request, "student.html", {'student': student,
                                            'studentDict': studentDict,
                                            'message': message})


def analysis(id_file, student_obj, name_file):
    """Evaluate and save the results in DB."""
    adapted_dict = {}
    num_pages = []
    sprites_tot = []
    text_sequences = []
    unedited_pages = []
    edited_pages = {}
    edited_sprites = {}
    unedited_sprites = []
    sprites_in_pages = {}
    sprites_same_name = {}

    pages_objs = Page.objects.all()
    for page in pages_objs:
        if page.mtime == id_file:
            num_pages.append(page.num_page)
            if len(page.background) < 30:
                unedited_pages.append(page.num_page)
            else:
                if page.num_page not in edited_pages:
                    edited_pages[page.num_page] = {}
                edited_pages[page.num_page] = page.background

    text_objs = Text.objects.all()
    for text in text_objs:
        if text.mtime == id_file:
            text_sequence = []
            text_sequence.append(text.page)
            text_sequence.append(text.id_name)
            text_sequence.append(["str_txt", text.str_txt])
            text_sequence.append(["fontsize", text.fontsize])
            text_sequences.append(text_sequence)

    sprites_objs = Sprite.objects.all()
    for sprite in sprites_objs:
        if sprite.mtime == id_file:
            sprites_tot.append(sprite.id_name)

            if len(sprite.looks) < 30:
                unedited_sprites.append(sprite.id_name)
            else:
                if sprite.id_name not in edited_sprites:
                    edited_sprites[sprite.id_name] = {}
                edited_sprites[sprite.id_name] = sprite.looks

            if sprite.page not in sprites_in_pages:
                sprites_in_pages[sprite.page] = []
            sprites_in_pages[sprite.page].append(sprite.name_sprite)

            array_script = []
            script = sprite.scripts
            script = script.replace(' ', '')
            script = eval(script.split()[0])
            array_script.append(script)
            array_script = array_script[0]
            if sprite.page not in adapted_dict:
                adapted_dict[sprite.page] = {}
            adapted_dict[sprite.page][sprite.id_name] = {}
            dict_sprite = adapted_dict[sprite.page][sprite.id_name]
            n = 0
            for sequence in array_script:
                n = n + 1
                for block in sequence:
                    block.pop(2)
                    block.pop(2)
                    sequence = "Sequence " + str(n)
                    if sequence not in dict_sprite:
                        dict_sprite[sequence] = []
                    dict_sprite[sequence].append(block)

    for page in sprites_in_pages:
        for name in sprites_in_pages[page]:
            if sprites_in_pages[page].count(name) > 1:
                if page not in sprites_same_name:
                    sprites_same_name[page] = {}
                sprites_same_name[page][name] = (sprites_in_pages[page].
                                                 count(name))

    total = analys_variability(adapted_dict)

    block_analy_obj = Block_analysis(student=student_obj,
                                     name_file=name_file, mtime=id_file,
                                     triggerings=triggerings(adapted_dict),
                                     motion=motion(adapted_dict),
                                     looks=looks(adapted_dict),
                                     control=control(adapted_dict),
                                     sound=sound(adapted_dict),
                                     ends=ends(adapted_dict), total=total)
    block_analy_obj.save()
    bad_habits_obj = Bad_habits(student=student_obj, name_file=name_file,
                                mtime=id_file, text_sequences=text_sequences,
                                deadcode=dead_code(adapted_dict),
                                unfinishedcode=unfinished_code(adapted_dict),
                                adjacentcode=equal_adjac_blocks(adapted_dict),
                                sprites_tot=sprites_tot, num_pages=num_pages,
                                unedited_sprites=unedited_sprites,
                                unedited_pages=unedited_pages,
                                sprites_in_pages=sprites_in_pages,
                                sprites_same_name=sprites_same_name,
                                edited_pages=edited_pages,
                                edited_sprites=edited_sprites)
    bad_habits_obj.save()

    # delete json data
    data_objs = Data.objects.all()
    data_objs.delete()
    pages_objs.delete()
    sprites_objs.delete()
    texts_objs = Text.objects.all()
    texts_objs.delete()


def analys_variability(adapted_dict):
    """Function.

    Returns the length of the total length of the Variability block types

    """
    variability_dict = {}
    variability_dict[_("Triggerings")] = triggerings(adapted_dict)
    variability_dict[_("Motion")] = motion(adapted_dict)
    variability_dict[_("Looks")] = looks(adapted_dict)
    variability_dict[_("Control")] = control(adapted_dict)
    variability_dict[_("Sound")] = sound(adapted_dict)
    variability_dict[_("Ends")] = ends(adapted_dict)

    # suma = 0.0
    total = 0
    for elem in variability_dict:
        # suma += float(len(variability_dict[elem])/len(_blocksDict[_(elem)]))
        total += len(variability_dict[elem])
    # average = round((suma * 10)/6, 2)
    return total


def triggerings(adapted_dict):
    """Function.

    Searches for Triggerings blocks and returns a list of the blocks found.

    """
    blocks = []
    if (find_block(adapted_dict, "onflag")):
        # Buscar un programa que tenga un bloque "onflag"
        blocks.append("onflag")
    if (find_block(adapted_dict, "onclick")):
        # Buscar un programa que tenga un bloque "onclick"
        blocks.append("onclick")
    if (find_block(adapted_dict, "ontouch")):
        # Buscar un programa que tenga un bloque "ontouch"
        blocks.append("ontouch")
    if (find_block(adapted_dict, "message")):
        # Buscar un programa que tenga un bloque "onclick"
        blocks.append("message")
    if (find_block(adapted_dict, "onmessage")):
        # Buscar un programa que tenga un bloque "ontouch"
        blocks.append("onmessage")
    # if (find_block_messages(adapted_dict, 1)):
    #     # Buscar un programa con "enviar mensaje" y otro porgrama con
    #     #  "comenzar con mensaje", ambos del mismo color)
    #     blocks.append("messages")
    return blocks


def motion(adapted_dict):
    """Function.

    Searches for Motion blocks and returns a list of the blocks found.

    """
    blocks = []
    if (find_block(adapted_dict, "left") or find_block(adapted_dict, "right")):
        # Buscar un programa que tenga un bloque "left" o "right"
        blocks.append("left-right")
    if (find_block(adapted_dict, "up") or find_block(adapted_dict, "down")):
        # Buscar un programa que tenga un bloque "up" o "down"
        blocks.append("up-down")
    if (find_block(adapted_dict, "forward") or
            find_block(adapted_dict, "back")):
        # Buscar un programa que tenga un bloque "forward" o "back"
        blocks.append("forward-back")
    if (find_block(adapted_dict, "hop")):
        # Buscar un programa que tenga un bloque "hop"
        blocks.append("hop")
    if (find_block(adapted_dict, "home")):
        # Buscar un programa que tenga un bloque "home"
        blocks.append("home")
    return blocks


def looks(adapted_dict):
    """Function.

    Searches for Looks blocks and returns a list of the blocks found.

    """
    blocks = []
    if (find_block(adapted_dict, "say")):
        # Buscar un programa que tenga un bloque "say"
        blocks.append("say")
    if (find_block(adapted_dict, "grow") or
            find_block(adapted_dict, "shrink")):
        # Buscar un programa que tenga un bloque "grow" o "shrink"
        blocks.append("grow-shrink")
    if (find_block(adapted_dict, "same")):
        # Buscar un programa que tenga un bloque "same"
        blocks.append("same")
    if (find_block(adapted_dict, "hide") or find_block(adapted_dict, "show")):
        # Buscar un programa que tenga un bloque "hide" o "show"
        blocks.append("hide-show")

    return blocks


def sound(adapted_dict):
    """Function.

    Searches for Sound blocks and returns a list of the blocks found.

    """
    blocks = []
    if (find_block(adapted_dict, "playsnd")):
        # Buscar un programa que tenga un bloque "playsnd"
        blocks.append("playsnd")
    if (find_block(adapted_dict, "playusersnd")):
        # Buscar un programa que tenga un bloque "playusersnd"
        blocks.append("playusersnd")
    return blocks


def control(adapted_dict):
    """Function.

    Searches for Control blocks and returns a list of the blocks found.

    """
    blocks = []
    if (find_block(adapted_dict, "wait")):
        # Buscar un programa que tenga un bloque "wait"
        blocks.append("wait")
    if (find_block(adapted_dict, "stopmine")):
        # Buscar un programa que tenga un bloque "stopmine"
        blocks.append("stopmine")
    if (find_block(adapted_dict, "setspeed")):
        # Buscar un programa que tenga un bloque "setspeed"
        blocks.append("setspeed")
    if (find_block(adapted_dict, "repeat")):
        # Buscar un programa que tenga un bloque "repeat"
        blocks.append("repeat")
    return blocks


def ends(adapted_dict):
    """Function.

    Searches for Ends blocks and returns a list of the blocks found.

    """
    blocks = []
    if (find_block(adapted_dict, "endstack")):
        # Buscar un programa que tenga un bloque "endstack"
        blocks.append("endstack")
    if (find_block(adapted_dict, "forever")):
        # Buscar un programa que tenga un bloque "forevery"
        blocks.append("forever")
    if (find_block(adapted_dict, "gotopage")):
        # Buscar un programa que tenga un bloque "gotopage"
        blocks.append("gotopage")
    return blocks


def find_block(adapted_dict, block):
    """Function searches for a block and returns True if found."""
    for pages in adapted_dict:
        for sprites in adapted_dict[pages]:
            for sequences in adapted_dict[pages][sprites]:
                for sequence in adapted_dict[pages][sprites][sequences]:
                    if sequence.count(block) == 1:
                        return True
                    go_over_repeat(sequence, block)
    return False


def go_over_repeat(sequence, block):
    """Function searches for a block within a Repeat block."""
    if sequence.count('repeat') == 1:
        for sequences_repeat in sequence:
            if isinstance(sequences_repeat, list):
                for sequence_repeat in sequences_repeat:
                    if sequence_repeat.count(block) == 1:
                        return True
                    go_over_repeat(sequence_repeat, block)


def dead_code(adapted_dict):
    """Function.

    Searches for sequences that don't start with an Triggering block,
     or searches for sequences that start with 'Start on Message' block of a
     color but no 'Send Message' block of the same color appears.

    """
    dead_sequences = []
    for pages in adapted_dict:
        for sprites in adapted_dict[pages]:
            for sequences in adapted_dict[pages][sprites]:
                triggering_found = False
                sequence = adapted_dict[pages][sprites][sequences][0]
                for block in triggering_blocks:
                    if sequence.count(block) == 1:
                        triggering_found = True
                        # Si no existe mensaje del mismo color...
                        if block == "onmessage":
                            found = False
                            for sprites1 in adapted_dict[pages]:
                                for sequences1 in (adapted_dict[pages]
                                                   [sprites1]):
                                    for sequence1 in (adapted_dict[pages]
                                                      [sprites1][sequences1]):
                                            if sequence1.count("message") == 1:
                                                if sequence[1] == sequence1[1]:
                                                    found = True
                            if not found:
                                triggering_found = False
                if not triggering_found:
                    dead_sequence = []
                    dead_sequence.append(pages)
                    dead_sequence.append(sprites)
                    dead_sequence.append(sequences)
                    seq = adapted_dict[pages][sprites][sequences]
                    dead_sequence.append(seq)
                    dead_sequences.append(dead_sequence)
    return dead_sequences


def unfinished_code(adapted_dict):
    """Function searches for sequences that don't end with an End block."""
    unfinished_sequences = []
    for pages in adapted_dict:
        for sprites in adapted_dict[pages]:
            for sequences in adapted_dict[pages][sprites]:
                triggering_found = False
                sequence = adapted_dict[pages][sprites][sequences][-1]
                for block in end_blocks:
                    if sequence.count(block) == 1:
                        triggering_found = True
                if not triggering_found:
                    unfinish_seq = []
                    unfinish_seq.append(pages)
                    unfinish_seq.append(sprites)
                    unfinish_seq.append(sequences)
                    seq = adapted_dict[pages][sprites][sequences]
                    unfinish_seq.append(seq)
                    unfinished_sequences.append(unfinish_seq)
    return unfinished_sequences


def equal_adjac_blocks(adapted_dict):
    """Function.

    Searches for sequences with repeating blocks together that can be replaced
     by a single block with attributes.

    """
    equal_blocks = False
    sequences_to_improve = []

    def adjacent_within_repeat(sequence):
        """Function.

        Searches for sequences with repeating blocks together that can be
         replaced by a single block with attributes within a "Repeat" block.

        """
        if sequence.count('repeat') == 1:
            previous_sequence = ""
            for sequences_repeat in sequence:
                if isinstance(sequences_repeat, list):
                    for sequence_repeat in sequences_repeat:
                        if sequence_repeat.count('repeat') == 1:
                            if adjacent_within_repeat(sequence_repeat):
                                return True
                        elif sequence_repeat[0] == previous_sequence:
                            return True
                        else:
                            previous_sequence = sequence_repeat[0]
        return False

    for pages in adapted_dict:
        for sprites in adapted_dict[pages]:
            for sequences in adapted_dict[pages][sprites]:
                previous_sequence = ""
                equal_blocks = False
                for sequence in adapted_dict[pages][sprites][sequences]:
                    if sequence.count('repeat') == 1:
                        if adjacent_within_repeat(sequence):
                            equal_blocks = True
                    elif sequence[0] == previous_sequence:
                        if sequence[0] in blocks_with_atrib:
                            equal_blocks = True
                    previous_sequence = sequence[0]
                if equal_blocks:
                    to_improve = []
                    to_improve.append(pages)
                    to_improve.append(sprites)
                    to_improve.append(sequences)
                    to_improve.append(adapted_dict[pages][sprites][sequences])
                    sequences_to_improve.append(to_improve)
    return sequences_to_improve


def delete_account(request):
    """View that builds the template account_deleted.html.

    Deletes all registered user data.

    """
    profile_user = User.objects.get(username=request.user)
    student_objs = Student.objects.filter(owner=request.user)
    for student_obj in student_objs:
        block_analy_obj = Block_analysis.objects.filter(student=student_obj)
        block_analy_obj.delete()
        bad_habits_obj = Bad_habits.objects.filter(student=student_obj)
        bad_habits_obj.delete()
        delete_files_student = StudentFiles.objects.filter(student=student_obj)
        delete_files_student.delete()
        student_obj.delete()
    profile_user.delete()

    return render(request, 'account_deleted.html', {})


def delete_filesbytime(path_folder, days):
    """Function deletes files that have a duration of 'days'."""
    # initializing the count
    deleted_files_count = 0
    deleted_folders_count = 0
    # duration in seconds
    seconds = time.time() - (days * 24 * 60 * 60)

    # checking whether the file is present in path or not
    if os.path.exists(path_folder):

        # iterating over each and every folder and file in the path
        for root_folder, folders, files in os.walk(path_folder):
            if path_folder[len(path_folder)-1] == '/':
                for file in files:

                    # file path
                    file_path = os.path.join(root_folder, file)
                    mtime = os.stat(file_path).st_mtime

                    # comparing the days
                    if seconds >= mtime:

                        # removing the file
                        if not os.remove(file_path):
                            # success message
                            deleted_files_count += 1  # incrementing count
                        else:
                            # failure message
                            print(f"Unable to delete the {file_path}")
            else:
                for folder in folders:
                    # folder path
                    folder_path = os.path.join(root_folder, folder)
                    mtime = os.stat(folder_path).st_mtime

                    # comparing the days
                    if seconds >= mtime:

                        # removing the folder
                        if not shutil.rmtree(folder_path):
                            # success message
                            deleted_folders_count += 1  # incrementing count
                        else:

                            # failure message
                            print(f"Unable to delete the {folder_path}")
    else:
        # file/folder is not found
        print(f'"{path_folder}" is not found')
