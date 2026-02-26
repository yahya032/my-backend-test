# admin.py
from django.contrib import admin
from .models import *

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_at']
    search_fields = ['name']

@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'university', 'code']
    list_filter = ['university']
    search_fields = ['name', 'code']

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'speciality', 'order']
    list_filter = ['speciality']
    search_fields = ['name']

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'level', 'order']
    list_filter = ['level']

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'semester', 'code', 'credits']
    list_filter = ['semester__level__speciality']
    search_fields = ['name']

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'matiere', 'file_type', 'download_count', 'created_at']
    list_filter = ['file_type', 'matiere__semester__level__speciality']
    search_fields = ['title']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'priority', 'is_global', 'created_at']
    list_filter = ['priority', 'is_global']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'first_name', 'last_name', 'email', 'university']
    search_fields = ['first_name', 'last_name', 'email']