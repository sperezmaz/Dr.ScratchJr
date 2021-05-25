from django.contrib import admin

from .models import Student, StudentFiles


class StudentFileInline(admin.TabularInline):
    model = StudentFiles
    extra = 2


class StudentAdmin(admin.ModelAdmin):
    inlines = [StudentFileInline, ]

admin.site.register(Student, StudentAdmin)
