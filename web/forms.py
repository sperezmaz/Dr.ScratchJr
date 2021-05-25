from django import forms


class UploadFilesForm(forms.Form):
    name_student = forms.CharField(max_length=50)
    file = forms.FileField()


class UploadFilesGuestForm(forms.Form):
    file = forms.FileField()

class UploadZipForm(forms.Form):
    file = forms.FileField()

class ProfileForm(forms.Form):
    first_name = forms.CharField(max_length=100)
    surname = forms.CharField(max_length=100)
    # message = forms.CharField(widget=forms.Textarea)

class FilesForm(forms.Form):
    student = forms.CharField(max_length=100)
    project = forms.CharField(max_length=100)
