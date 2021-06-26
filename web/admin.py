from django.contrib import admin

from .models import Student, Project


class ProjectInline(admin.TabularInline):
    model = Project
    extra = 2


class StudentAdmin(admin.ModelAdmin):
    inlines = [ProjectInline, ]

admin.site.register(Student, StudentAdmin)
