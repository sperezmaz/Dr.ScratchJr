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
from .models import Variability, Bad_habits, Creativity, Other_data
from .models import Analysis_types
from .models import Student, Project
from .models import Files_zip, Zip
from django.contrib.auth.models import User
from django.forms import formset_factory
from .forms import UploadFilesForm, UploadFilesGuestForm, ProfileForm
from .forms import UploadZipForm, FilesForm1, FilesForm2
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

    name_studentfiles = Project.objects.all()
    html += "<p>--------------------------------Listado de Project: </p>"
    for obj in name_studentfiles:
        html += '<p>' + str(obj) + '<p>'
        html += '<p>' + str(obj.student) + '<p>'
        html += '<p>' + str(obj.file_up) + '<p>'
        html += '<p>' + str(obj.timestamp) + '<p>'
        html += '<p> mtime: ' + str(obj.mtime) + '<p>'

    variability_obj = Variability.objects.all()
    html += "<p>-----Listado de Variability (student, mtime y name): </p>"
    for obj in variability_obj:
        html += '<p> project: ' + str(obj.project) + '<p>'
        html += '<p> triggerings: ' + str(obj.triggerings) + '<p>'
        html += '<p> updated: ' + str(obj.updated) + '<p>'
    
    zip_obj = Zip.objects.all()
    html += "<p>-----Listado de Zip (zip_name): </p>"
    for obj in zip_obj:
        html += '<p> zip_name: ' + str(obj.zip_name) + '<p>'
        html += '<p> project: ' + str(obj.project) + '<p>'
        html += '<p> project_name: ' + str(obj.project_name) + '<p>'

    name_files = Files_zip.objects.all()
    html += "<p>------------------------------------Listado de Files_zip: </p>"
    for obj2 in name_files:
        html += '<p>' + str(obj2.zip_up) + '<p>'

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


def variability_view(request):
    """View that builds the template variability.html."""
    _blocksDict = {}

    for typess in blocksDict:
        if typess == 'Total':
            pass
        else:
            _blocksDict[_(typess)] = blocksDict[typess]
    return render(request, "variability.html", {'blocksDict': _blocksDict})


def bad_habits_view(request):
    """View that builds the template bad_habits.html."""
    return render(request, "bad_habits.html", {})


def copy_files_creativity(folder_creativ, folder_proj):
    """Function copies edited files to a Creativity folder."""
    if not os.path.exists('web/static/plugins/creativity/'):
        os.mkdir('web/static/plugins/creativity/')

    try:
        contenidos = os.listdir(folder_proj + '/project/' + folder_creativ)
        for elemento in contenidos:
            shutil.copy2(folder_proj + '/project/' + folder_creativ + '/' +
                         elemento, 'web/static/plugins/creativity/')
    except:
        pass


def extract_data(project_obj):
    """Function extracts zip, opens json.

    Stores the analyzed data if no data exists.

    Then returns the analyzed data.

    """
    name_file = str(project_obj.file_up).split("/")[3]
    folder_file_up = str(project_obj.file_up).split(name_file)[0]
    folder_proj = folder_file_up + 'uncompress_folder'
    # unzip file
    zf = zipfile.ZipFile(str(project_obj.file_up), "r")
    for i in zf.namelist():
        zf.extract(i, folder_proj)
    zf.close()

    # delete uploaded file_up
    if os.path.exists(str(project_obj.file_up)):
        remove(str(project_obj.file_up))

    copy_files_creativity("characters", folder_proj)
    copy_files_creativity("backgrounds", folder_proj)
    copy_files_creativity("sounds", folder_proj)

    # extract data from json
    with open(folder_proj + '/project/data.json', encoding="utf8") as file:
        data = json.load(file)
        mtime = data['mtime']
        project_obj.mtime = mtime
        project_obj.file_up = name_file
        project_obj.save(update_fields=['file_up', 'mtime'])

        if project_obj.student is not None:
            # save json data
            project_obj = save_file(project_obj)

        file_name = project_obj.file_up

        try:
            variability_obj = Variability.objects.get(project=project_obj)
            variability_obj.save()
        except ObjectDoesNotExist:
            # save data if there isn´t data is stored
            save_data(data)
            analysis(project_obj)

        # extracts analyzed data
        (variability_dict, badhabits_dict, otherdat_dict, creativ_dict) = \
            extract_analysis(project_obj)

        # delete projects without student
        if project_obj.student is None:
            project_obj.delete()

    # delete uploaded folder
    if os.path.exists(folder_file_up):
        shutil.rmtree(folder_file_up)

    return (file_name, mtime, variability_dict, badhabits_dict, otherdat_dict,
            creativ_dict)


def open_projects_in_zip(request, f, zip_proj, path_folder):
    """Function opens json.

    Stores the analyzed data if no data exists.

    """
    copy_files_creativity("characters", path_folder)
    copy_files_creativity("backgrounds", path_folder)
    copy_files_creativity("sounds", path_folder)

    with open(path_folder + '/project/data.json',
              encoding="utf8") as file:
        data = json.load(file)
        mtime = data['mtime']
        file_name = f.cleaned_data['project'] + ".sjr"
        # save if user is authenticated
        if not request.user.is_authenticated:
            project_obj = Project(file_up=file_name, mtime=mtime)
            project_obj.save()
        elif request.user.is_authenticated:
            student_name = f.cleaned_data['student']
            if Student.objects.filter(owner=request.user,
                                      title=student_name).exists():
                # authenticated and student name exists
                student_obj = Student.objects.get(owner=request.user,
                                                  title=student_name)
                project_obj = Project(student=student_obj, file_up=file_name,
                                      mtime=mtime)
            else:
                # authenticated and new student name
                student_obj = Student(owner=request.user,
                                      title=student_name)
                student_obj.save()
                project_obj = Project(student=student_obj, file_up=file_name,
                                      mtime=mtime)
            project_obj.save()
            save_file(project_obj)
        zip_proj.project = project_obj
        zip_proj.save(update_fields=['project'])

        try:
            variability_obj = Variability.objects.get(project=project_obj)
            variability_obj.save()
        except ObjectDoesNotExist:
            # save data if there isn´t data is stored
            save_data(data)
            analysis(project_obj)


def create_csv_zip(request, zip_name, rand_folder):
    """Function gets object from the stored zip.

    Creates csv and xlsx files with all the analyzed data of all the projects
     that had the object.

    Returns the csv and xlsx files compressed in a zip file.

    """
    project_objs = Zip.objects.filter(zip_name=zip_name,
                                      rand_folder=rand_folder)
    letters = string.ascii_letters
    rand_folder = ''.join(random.choice(letters) for _ in range(6))
    folder_upload = "web/csv/" + rand_folder + '/'
    zip = zip_name.split(".zip")[0]
    project_folder = folder_upload + zip
    create_csv(project_objs, zip, folder_upload, project_folder, True)
    response = FileResponse(open(folder_upload + zip + ".zip", 'rb'))
    return response


def create_csv_student(request, student):
    """Function gets object from the stored student.

    Creates csv and xlsx files with all the analyzed data of all the projects
     that had the object.

    Returns the csv and xlsx files compressed in a zip file.

    """
    student_obj = Student.objects.get(owner=request.user, title=student)
    project_obj = Project.objects.filter(student=student_obj)
    letters = string.ascii_letters
    rand_folder = ''.join(random.choice(letters) for _ in range(6))
    folder_upload = "web/csv/" + rand_folder + '/'
    project_folder = folder_upload + student
    create_csv(project_obj, student, folder_upload, project_folder, False)
    response = FileResponse(open(folder_upload + student + ".zip", 'rb'))
    return response


def create_csv_user(request):
    """Function gets object from the stored user.

    Creates csv and xlsx files with all the analyzed data of all the projects
     that had the object.

    Returns the csv and xlsx files compressed in a zip file.

    """
    project_obj = []
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
        project_obj = Project.objects.filter(student=student_obj)
        for file_obj in project_obj:
            stud_name = file_obj.student.title
            file_name = file_obj.file_up

            (variability_dict, badhabits_dict, otherdat_dict, creativ_dict) = \
                extract_analysis(file_obj)

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


def create_csv(project_objs, name_zip_csv, folder_upload, project_folder, is_zip):
    """Function.

    Creates csv and xlsx files with all the analyzed data (variability,
     badhabits and otherdata) of all the projects (project_objs).

    """
    bad_habits_dict = {}
    os.makedirs(project_folder, exist_ok=True)
    variability_path = project_folder + "/variability-%s.csv"
    variability_path = next_path(variability_path)
    bad_habits_path = project_folder + "/badhabits-%s.csv"
    bad_habits_path = next_path(bad_habits_path)
    other_data_path = project_folder + "/otherdata-%s.csv"
    other_data_path = next_path(other_data_path)
    for project_obj in project_objs:
        if is_zip:
            project_obj = project_obj.project
            if project_obj.student is None:
                stud_name = "-"
            else:
                stud_name = project_obj.student.title
        else:
            stud_name = project_obj.student.title
        file_name = project_obj.file_up

        (variability_dict, badhabits_dict, otherdat_dict, creativ_dict) = \
            extract_analysis(project_obj)

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

    shutil.copy2("web/csv/README.txt", folder_upload + name_zip_csv)

    # delete zips old (30 min)
    delete_filesbytime("web/csv", 1/48)

    fantasy_zip = zipfile.ZipFile(folder_upload + name_zip_csv + ".zip", 'w')

    for folder, subfolders, files in os.walk(project_folder):
        for file in files:
            fantasy_zip.write(os.path.join(folder, file),
                              os.path.relpath(os.path.join(folder, file),
                                              project_folder),
                              compress_type=zipfile.ZIP_DEFLATED)
    writer.close()
    # delete folder
    if os.path.exists(folder_upload + name_zip_csv):
        shutil.rmtree(folder_upload + name_zip_csv)


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
    fieldnames = [_('Name'), _('Project name'), _('Type of bad habit'),
                  _('Existence bad habit'), _('Page'), _('Character'),
                  _('Sequence name'), _('Sequence'),
                  _("Characters same name in page")]

    for clave in badhabits_dict:
        bad_habits_dict[_("Type of bad habit")] = clave
        if badhabits_dict[clave] == [] or badhabits_dict[clave] == {}:
            bad_habits_dict[_("Existence bad habit")] = _("NONE")
            bad_habits_dict[_("Page")] = "----"
            bad_habits_dict[_("Character")] = "----"
            bad_habits_dict[_("Sequence name")] = "----"
            bad_habits_dict[_("Sequence")] = "----"
            bad_habits_dict[_("Characters same name in page")] = "----"
            write_csv(bad_habits_path, fieldnames, bad_habits_dict)
        elif type(badhabits_dict[clave]) is dict:
                bad_habits_dict[_("Existence bad habit")] = _("YES")
                bad_habits_dict[_("Page")] = "----"
                bad_habits_dict[_("Character")] = "----"
                bad_habits_dict[_("Sequence name")] = "----"
                bad_habits_dict[_("Sequence")] = "----"
                bad_habits_dict[_("Characters same name in page")] = \
                    badhabits_dict[clave]
                write_csv(bad_habits_path, fieldnames, bad_habits_dict)
        else:
            for elem in badhabits_dict[clave]:
                bad_habits_dict[_("Existence bad habit")] = _("YES")
                bad_habits_dict[_("Page")] = elem[0]
                bad_habits_dict[_("Character")] = elem[1]
                bad_habits_dict[_("Sequence name")] = elem[2]
                bad_habits_dict[_("Sequence")] = elem[3]
                bad_habits_dict[_("Characters same name in page")] = "----"
                write_csv(bad_habits_path, fieldnames, bad_habits_dict)


def other_data_csv(otherdat_dict, other_data_path):
    """Function adapts otherdat_dict to create csv file."""
    fieldnames = [_('Name'), _('Project name'), _('Total pages'), _('Pages'),
                  _('Total characters'), _('Characters'), _("Total texts"),
                  _("Texts in pages"),
                  _('Total pages with unedited background'),
                  _('Pages with unedited background'),
                  _('Total unedited characters'), _('Unedited characters'),
                  _('Characters in pages')]

    otherdat_dict[_("Pages")] = str(otherdat_dict[_("Total pages")])
    otherdat_dict[_("Total pages")] = len(otherdat_dict[_("Total pages")])
    otherdat_dict[_("Characters")] = str(otherdat_dict[_("Total characters")])
    otherdat_dict[_("Total characters")] = \
        len(otherdat_dict[_("Total characters")])
    otherdat_dict[_("Texts in pages")] = str(otherdat_dict[_("Total texts")])
    otherdat_dict[_("Total texts")] = len(otherdat_dict[_("Total texts")])
    otherdat_dict[_("Total pages with unedited background")] = \
        len(otherdat_dict[_("Pages with unedited background")])
    otherdat_dict[_("Total unedited characters")] = \
        len(otherdat_dict[_("Unedited characters")])
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


def save_file(stdnt_files_obj):
    """Function renames repeated files and saves file data with the student."""
    studentDict = []
    name_studentfiles = Project.objects.all()
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
                stdnt_files_obj.save(update_fields=['file_up'])
    return stdnt_files_obj


def save_data(data):
    """Function saves json data in DB (Data, Page, Sprite and Text)."""
    ctime = data['ctime']
    mtime = data['mtime']
    name_project = data['name']
    pages = data['json']['pages']
    pagecount = data['thumbnail']['pagecount']
    version = data['version']
    currentpage = data['json']['currentPage']

    archivo = Data(ctime=ctime, mtime=mtime, name_project=name_project,
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


def extract_analysis(project_obj):
    """Function extracts the analysis data from the DB.

    Returns the dictionaries (variability_dict, badhabits_dict, otherdat_dict,
     creativ_dict) of the analysis.

    """
    variability_dict = {}
    badhabits_dict = {}
    otherdata_dict = {}
    creativ_dict = {}
    variability_obj = Variability.objects.get(project=project_obj)
    badhabits_obj = Bad_habits.objects.get(project=project_obj)
    creativity_obj = Creativity.objects.get(project=project_obj)
    other_data_obj = Other_data.objects.get(project=project_obj)

    variability_dict[_("Triggerings")] = eval(variability_obj.triggerings)
    variability_dict[_("Motion")] = eval(variability_obj.motion)
    variability_dict[_("Looks")] = eval(variability_obj.looks)
    variability_dict[_("Control")] = eval(variability_obj.control)
    variability_dict[_("Sound")] = eval(variability_obj.sound)
    variability_dict[_("Ends")] = eval(variability_obj.ends)

    variability_dict["Total"] = variability_obj.total

    badhabits_dict[_("Dead code")] = eval(badhabits_obj.deadcode)
    badhabits_dict[_("Unfinished code")] = eval(badhabits_obj.unfinishedcode)
    badhabits_dict[_("Sequences with adjacent blocks")] = \
        eval(badhabits_obj.adjacentcode)
    badhabits_dict[_("Characters same name in page")] = \
        eval(badhabits_obj.sprites_same_name)

    otherdata_dict[_("Total pages")] = eval(other_data_obj.pages_tot)
    otherdata_dict[_("Total characters")] = eval(other_data_obj.sprites_tot)
    otherdata_dict[_("Total texts")] = eval(other_data_obj.text_sequences)
    otherdata_dict[_("Pages with unedited background")] = \
        eval(other_data_obj.unedited_pages)
    otherdata_dict[_("Unedited characters")] = \
        eval(other_data_obj.unedited_sprites)
    otherdata_dict[_("Characters in pages")] = \
        eval(other_data_obj.sprites_in_pages)

    creativ_dict[_("Edited pages")] = eval(creativity_obj.edited_pages)
    creativ_dict[_("Edited characters")] = eval(creativity_obj.edited_sprites)
    creativ_dict[_("Sounds created")] = \
        eval(creativity_obj.sprites_sound_created)

    return variability_dict, badhabits_dict, otherdata_dict, creativ_dict


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
    mtime = ""
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
                name_student = form.cleaned_data['name_student']
            except:
                pass

            if (str(request.FILES['file']).find(".sjr") != -1):
                file_up = request.FILES['file']

                if not request.user.is_authenticated:
                    # if not authenticated only save file
                    project_obj = Project(file_up=file_up)
                elif Student.objects.filter(owner=request.user,
                                            title=name_student).exists():
                    # authenticated and student name exists
                    student_obj = Student.objects.get(owner=request.user,
                                                      title=name_student)
                    project_obj = Project(student=student_obj,
                                             file_up=file_up)
                else:
                    # authenticated and new student name
                    student_obj = Student(owner=request.user,
                                          title=name_student)
                    student_obj.save()
                    project_obj = Project(student=student_obj,
                                             file_up=file_up)
                project_obj.save()
                message = _("File uploaded succesfully!")

                # extract data from uploaded file
                (name, mtime, variability_d, badhabits_d, otherdat_d,
                 creativ_d) = extract_data(project_obj)

                save_analys(str(name), mtime, variability_d, badhabits_d,
                            otherdat_d, creativ_d)

                character_sounds = creativ_d[_('Sounds created')]
                list_sounds = []
                for sounds in character_sounds.values():
                    for sound_elem in sounds:
                        list_sounds.append(sound_elem)
                creativ_d[_('Sounds created')] = list_sounds

                # delete edited images/sounds after 1 year
                delete_filesbytime('web/static/plugins/creativity/', 365)

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
    list_projects = []
    elementos = []
    FileFormSet1 = formset_factory(FilesForm1, extra=0)
    FileFormSet2 = formset_factory(FilesForm2, extra=0)

    if request.method == 'POST':
        form = UploadZipForm(request.POST, request.FILES)
        formset1 = FileFormSet1(request.POST)
        formset2 = FileFormSet2(request.POST)
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
                        if request.user.is_authenticated:
                            project = elemento.split("-")[0]
                            student = elemento.split("-")[1]
                            student = student.split(".sjr")[0]
                            projects_dict = {}
                            projects_dict['student'] = str(student)
                            projects_dict['project'] = str(project)
                            projects_dict['unzip_folder'] = unzip_folder
                            inicial_form.append(projects_dict)
                        else:
                            student = ""
                            project = elemento.split(".sjr")[0]
                            projects_dict = {}
                            projects_dict['project'] = str(project)
                            projects_dict['unzip_folder'] = unzip_folder
                            inicial_form.append(projects_dict)
                        elementos.append(elemento)
                        project_obj = Zip(zip_name=file_up,
                                          project_name=elemento,
                                          rand_folder=rand_folder)
                        project_obj.save()
                except:
                    message = "Projects must be named as indicated in the form"
                    message += " description"
                    message = _(message)
                    form = UploadZipForm()
                    return render(request, 'up_zip.html', {'form': form,
                                                           'message': message})
                if request.user.is_authenticated:
                    formset = FileFormSet2(initial=inicial_form)
                else:
                    formset = FileFormSet1(initial=inicial_form)
                return render(request, 'up_zip.html', {'formset': formset,
                                                       'message': message,
                                                       'elementos': elementos})

            elif str(request.FILES['file']).find(".zip") == -1:
                message = _("The file must have the extension .zip!")
        elif not form.is_valid():
            if request.user.is_authenticated:
                formset = formset2
            else:
                formset = formset1
            
            if formset.is_valid():
                n = 0
                for f in formset:
                    # update data with formset
                    unzip_folder = f.cleaned_data['unzip_folder']
                    rand_folder = unzip_folder.split('/')[-2]
                    contenidos = os.listdir(unzip_folder + 'proj')
                    name = str(contenidos[n])
                    zip_obj = Zip.objects.get(project_name=name,
                                              rand_folder=rand_folder)

                    # extract projects
                    path_files = unzip_folder + 'proj/' + contenidos[n]
                    zf = zipfile.ZipFile(path_files, "r")
                    folder = str(contenidos[n].split(".sjr")[0])
                    path_folder = unzip_folder + 'projs/' + folder
                    for i in zf.namelist():
                        zf.extract(i, path_folder)
                    n += 1
                    open_projects_in_zip(request, f, zip_obj, path_folder)
                    projects_dict = {}
                    if request.user.is_authenticated:
                        student = f.cleaned_data['student']
                    else:
                        student = "-"
                    projects_dict[student] = \
                        [str(f.cleaned_data['project']), 
                         str(zip_obj.project_name)]
                    list_projects.append(projects_dict)
                zf.close()
                # delete uploaded folder
                if os.path.exists(unzip_folder):
                    shutil.rmtree(unzip_folder)

                return render(request, 'review_zip.html',
                              {'zip_name': zip_obj.zip_name,
                               'list_projects': list_projects,
                               'rand_folder': rand_folder,
                               'message': message})
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

    fileszip_objs_all = Zip.objects.all()
    for fileszip_objs in fileszip_objs_all:
        time_file = get_time(fileszip_objs.timestamp)
        if seconds >= time_file:
            if fileszip_objs.project != None:
                if fileszip_objs.project.student is None:
                    fileszip_objs.project.delete()

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


def analysis_view(request, student, name_file):
    """View that builds the template analysis.html.

    Extracts analysis and saves it in the DB.

    """
    _blocksDict = {}
    student_obj = Student.objects.get(owner=request.user, title=student)
    project_obj = Project.objects.get(student=student_obj, file_up=name_file)

    (variab_dict, badhabit_dict, otherdat_dict, creativ_dict) = \
        extract_analysis(project_obj)

    save_analys(str(project_obj.file_up), project_obj.mtime, variab_dict,
                badhabit_dict, otherdat_dict, creativ_dict)

    character_sounds = creativ_dict[_('Sounds created')]
    list_sounds = []
    for sounds in character_sounds.values():
        for sound_elem in sounds:
            list_sounds.append(sound_elem)
    creativ_dict[_('Sounds created')] = list_sounds

    for typess in blocksDict:
        _blocksDict[_(typess)] = blocksDict[typess]

    return render(request, "analysis.html", {'file_up': project_obj.file_up,
                                             'mtime': project_obj.mtime,
                                             'variability_dict': variab_dict,
                                             'badhabits_dict': badhabit_dict,
                                             'otherdat_dict': otherdat_dict,
                                             'creativ_dict': creativ_dict,
                                             'blocksDict': _blocksDict})


def analysis2_view(request, student, project, file_name, rand_folder):
    """View that builds the template analysis.html.

    Extracts analysis and saves it in the DB.

    """
    _blocksDict = {}
    if request.user.is_authenticated:
        student_obj = Student.objects.get(owner=request.user, title=student)
        project = project + ".sjr"
        project_obj = Project.objects.get(student=student_obj, file_up=project)
    else:
        zip_proj_obj = Zip.objects.get(rand_folder=rand_folder,
                                       project_name=file_name)
        project_obj = zip_proj_obj.project

    (variab_dict, badhabit_dict, otherdat_dict, creativ_dict) = \
        extract_analysis(project_obj)

    save_analys(project_obj.file_up, project_obj.mtime, variab_dict,
                badhabit_dict, otherdat_dict, creativ_dict)

    character_sounds = creativ_dict[_('Sounds created')]
    list_sounds = []
    for sounds in character_sounds.values():
        for sound_elem in sounds:
            list_sounds.append(sound_elem)
    creativ_dict[_('Sounds created')] = list_sounds

    for typess in blocksDict:
        _blocksDict[_(typess)] = blocksDict[typess]

    return render(request, "analysis.html", {'file_up': project_obj.file_up,
                                             'mtime': project_obj.mtime,
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

@login_required
def settings_view(request):
    """View that builds the template settings.html."""
    return render(request, "settings.html", {})

@login_required
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
        file_objects = Project.objects.filter(student=student_obj)
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
    file_objects = Project.objects.filter(student=student_obj)
    for file_obj in file_objects:
        timestamp1 = str(file_obj.timestamp)
        timestamp1 = str(timestamp1.split(".")[0])
        file_up = str(file_obj.file_up)

        variability_obj = Variability.objects.get(project=file_obj)
        bad_habits_obj = Bad_habits.objects.get(project=file_obj)
        total = str(variability_obj.total) + '/' + str(blocksDict['Total'])
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
    delete_file = Project.objects.get(student=student_obj,
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
    delete_files_student = Project.objects.filter(student=student_obj)
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
    if Project.objects.filter(student=student_obj,
                                   file_up=new_file).exists():
        message = _("Error: The file name is already in use!")
    else:
        file_obj = Project.objects.get(student=student_obj,
                                            file_up=old_file)
        file_obj.file_up = new_file
        file_obj.save(update_fields=['file_up'])
        message = _("File edit succesfully!")
    studentDict = student_dict(request, student)
    return render(request, "student.html", {'student': student,
                                            'studentDict': studentDict,
                                            'message': message})


def analysis(project_obj):
    """Evaluate and save the results in DB."""
    adapted_dict = {}
    num_pages = []
    sprites_tot = []
    text_sequences = []
    unedited_pages = []
    edited_pages = {}
    edited_sprites = {}
    sprites_sound_created = {}
    unedited_sprites = []
    sprites_in_pages = {}
    sprites_same_name = {}
    variability_dict = {}

    pages_objs = Page.objects.all()
    for page in pages_objs:
        if page.mtime == project_obj.mtime:
            num_pages.append(page.num_page)
            if len(page.background) < 30:
                unedited_pages.append(page.num_page)
            else:
                if page.num_page not in edited_pages:
                    edited_pages[page.num_page] = {}
                edited_pages[page.num_page] = page.background

    text_objs = Text.objects.all()
    for text in text_objs:
        if text.mtime == project_obj.mtime:
            text_sequence = []
            text_sequence.append(text.page)
            text_sequence.append(text.id_name)
            text_sequence.append(["str_txt", text.str_txt])
            text_sequence.append(["fontsize", text.fontsize])
            text_sequences.append(text_sequence)

    sprites_objs = Sprite.objects.all()
    for sprite in sprites_objs:
        if sprite.mtime == project_obj.mtime:
            names_sprites = sprite.name_sprite + ' (' + sprite.id_name + ')'
            sprites_tot.append(names_sprites)

            if len(sprite.looks) < 30:
                unedited_sprites.append(names_sprites)
            else:
                if names_sprites not in edited_sprites:
                    edited_sprites[names_sprites] = {}
                edited_sprites[names_sprites] = sprite.looks

            sounds = eval(sprite.sounds)
            for sound_elem in sounds:
                if len(sound_elem) >= 30:
                    if names_sprites not in sprites_sound_created:
                        sprites_sound_created[names_sprites] = []
                    sprites_sound_created[names_sprites].append(sound_elem)

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
            adapted_dict[sprite.page][names_sprites] = {}
            dict_sprite = adapted_dict[sprite.page][names_sprites]
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
            count_ = sprites_in_pages[page].count(name)
            if count_ > 1:
                if page not in sprites_same_name:
                    sprites_same_name[page] = {}
                sprites_same_name[page][name] = str(count_) + _(" occasions")


    variability_dict[_("Triggerings")] = triggerings(adapted_dict)
    variability_dict[_("Motion")] = motion(adapted_dict)
    variability_dict[_("Looks")] = looks(adapted_dict)
    variability_dict[_("Control")] = control(adapted_dict)
    variability_dict[_("Sound")] = sound(adapted_dict)
    variability_dict[_("Ends")] = ends(adapted_dict)

    variability_obj = Variability(project=project_obj,
                                  triggerings=variability_dict[_("Triggerings")],
                                  motion=variability_dict[_("Motion")],
                                  looks=variability_dict[_("Looks")],
                                  control=variability_dict[_("Control")],
                                  sound=variability_dict[_("Sound")],
                                  ends=variability_dict[_("Ends")], 
                                  total=analys_variability(variability_dict))
    variability_obj.save()
    bad_habits_obj = Bad_habits(project=project_obj,
                                deadcode=dead_code(adapted_dict),
                                unfinishedcode=unfinished_code(adapted_dict),
                                adjacentcode=equal_adjac_blocks(adapted_dict),
                                sprites_same_name=sprites_same_name)
    bad_habits_obj.save()
    creativity_obj = Creativity(project=project_obj, edited_pages=edited_pages,
                                edited_sprites=edited_sprites,
                                sprites_sound_created=sprites_sound_created)
    creativity_obj.save()
    other_data_obj = Other_data(project=project_obj,
                                text_sequences=text_sequences,
                                sprites_tot=sprites_tot, pages_tot=num_pages,
                                unedited_sprites=unedited_sprites,
                                unedited_pages=unedited_pages,
                                sprites_in_pages=sprites_in_pages)
    other_data_obj.save()
    # delete json data
    data_objs = Data.objects.all()
    data_objs.delete()
    pages_objs.delete()
    sprites_objs.delete()
    text_objs.delete()


def analys_variability(variability_dict):
    """Function.

    Returns the length of the total length of the Variability block types

    """


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
        # Buscar un programa que tenga un bloque "onmessage"
        blocks.append("onmessage")
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
                    if go_over_repeat(sequence, block):
                        return True
    return False


def go_over_repeat(sequence, block):
    """Function searches for a block within a Repeat block."""
    if sequence.count('repeat') == 1:
        for sequences_repeat in sequence:
            if isinstance(sequences_repeat, list):
                for sequence_repeat in sequences_repeat:
                    if sequence_repeat.count(block) == 1:
                        return True
                    if go_over_repeat(sequence_repeat, block):
                        return True


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
        delete_files_student = Project.objects.filter(student=student_obj)
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
