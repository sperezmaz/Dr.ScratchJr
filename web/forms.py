from django import forms
from .models import Contact


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


class FilesForm1(forms.Form):
    project = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    unzip_folder = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type': 'hidden'}))


class FilesForm2(forms.Form):
    student = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    project = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control'}))
    unzip_folder = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'type': 'hidden'}))


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'