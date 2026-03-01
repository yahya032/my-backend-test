from django.contrib import admin
from .models import *

@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'logo_url', 'calendar_url', 'created_at']
    list_display_links = ['name']
    search_fields = ['name']
    list_filter = ['created_at']
    fieldsets = (
        ('Informations principales', {
            'fields': ('name', 'description')
        }),
        ('URLs', {
            'fields': ('logo_url', 'calendar_url'),
            'classes': ('wide',),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'university', 'code', 'created_at']
    list_display_links = ['name']
    list_filter = ['university', 'created_at']
    search_fields = ['name', 'code']
    autocomplete_fields = ['university']
    fieldsets = (
        ('Informations', {
            'fields': ('university', 'name', 'code', 'description')
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'get_name_display', 'speciality', 'order', 'created_at']
    list_display_links = ['name']
    list_filter = ['speciality__university', 'speciality', 'name']
    search_fields = ['speciality__name', 'code']
    autocomplete_fields = ['speciality']
    list_editable = ['order']
    
    fieldsets = (
        ('Informations', {
            'fields': ('speciality', 'name', 'code', 'description', 'order')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ['created_at']


@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'level', 'order', 'created_at']
    list_display_links = ['name']
    list_filter = ['level__speciality__university', 'level__speciality', 'level']
    search_fields = ['name', 'code']
    autocomplete_fields = ['level']
    list_editable = ['order']
    
    fieldsets = (
        ('Informations', {
            'fields': ('level', 'name', 'code', 'order')
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ['created_at']


@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'semester', 'credits', 'coefficient', 'created_at']
    list_display_links = ['name']
    list_filter = ['semester__level__speciality__university', 'semester__level__speciality', 'semester__level']
    search_fields = ['name', 'code', 'description']
    autocomplete_fields = ['semester']
    list_editable = ['credits', 'coefficient']
    
    fieldsets = (
        ('Informations', {
            'fields': ('semester', 'name', 'code', 'description')
        }),
        ('Paramètres pédagogiques', {
            'fields': ('credits', 'coefficient'),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'matiere', 'document_type', 'file_type', 
        'download_count', 'is_published', 'created_at'
    ]
    list_display_links = ['title']
    list_filter = [
        'document_type', 'file_type', 'is_published',
        'matiere__semester__level__speciality__university',
        'matiere__semester__level__speciality',
        'created_at'
    ]
    search_fields = ['title', 'description']
    autocomplete_fields = ['matiere']
    list_editable = ['is_published']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Document', {
            'fields': ('matiere', 'title', 'description', 'file')
        }),
        ('Classification', {
            'fields': ('document_type', 'file_type'),
        }),
        ('Publication', {
            'fields': ('is_published', 'download_count'),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ['download_count', 'created_at', 'updated_at']
    
    actions = ['publish_documents', 'unpublish_documents', 'reset_download_count']
    
    def publish_documents(self, request, queryset):
        queryset.update(is_published=True)
        self.message_user(request, f"{queryset.count()} documents publiés")
    publish_documents.short_description = "Publier les documents sélectionnés"
    
    def unpublish_documents(self, request, queryset):
        queryset.update(is_published=False)
        self.message_user(request, f"{queryset.count()} documents dépubliés")
    unpublish_documents.short_description = "Dépublier les documents sélectionnés"
    
    def reset_download_count(self, request, queryset):
        queryset.update(download_count=0)
        self.message_user(request, f"Compteurs remis à zéro pour {queryset.count()} documents")
    reset_download_count.short_description = "Remettre à zéro les compteurs de téléchargement"
    
    def get_changeform_initial_data(self, request):
        return {
            'document_type': 'CM',
            'file_type': 'pdf',
            'is_published': True,
        }


@admin.register(FavoriteDocument)
class FavoriteDocumentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'document', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user_id', 'document__title']
    autocomplete_fields = ['document']
    date_hierarchy = 'created_at'


@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'priority', 'is_global', 'user_id', 'created_at']
    list_display_links = ['title']
    list_filter = ['priority', 'is_global', 'created_at', 'university', 'speciality', 'level']
    search_fields = ['title', 'message', 'user_id']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Message', {
            'fields': ('title', 'message', 'priority')
        }),
        ('Ciblage', {
            'fields': ('is_global', 'user_id', 'university', 'speciality', 'level'),
        }),
        ('Durée', {
            'fields': ('expires_at',),
        }),
        ('Métadonnées', {
            'fields': ('created_at',),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ['created_at']


@admin.register(AlertReadStatus)
class AlertReadStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'alert', 'user_id', 'is_read', 'read_at']
    list_filter = ['is_read', 'read_at']
    search_fields = ['user_id', 'alert__title']
    autocomplete_fields = ['alert']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'email', 'first_name', 'last_name', 'university', 'created_at']
    list_display_links = ['email']
    list_filter = ['university', 'speciality', 'level', 'created_at']
    search_fields = ['user_id', 'email', 'first_name', 'last_name', 'phone']
    autocomplete_fields = ['university', 'speciality', 'level']
    
    fieldsets = (
        ('Compte Firebase', {
            'fields': ('user_id', 'email')
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'phone', 'photo_url')
        }),
        ('Parcours', {
            'fields': ('university', 'speciality', 'level'),
        }),
        ('Métadonnées', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ['created_at', 'updated_at']


@admin.register(UserUniversity)
class UserUniversityAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'university', 'created_at']
    list_filter = ['university', 'created_at']
    search_fields = ['user_id', 'university__name']
    autocomplete_fields = ['university']
    date_hierarchy = 'created_at'