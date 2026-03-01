from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse, path
from django.db.models import Count, Sum  # ← AJOUTER Sum ICI
from django.template.response import TemplateResponse
from django.http import JsonResponse
from django.utils import timezone  # ← AJOUTER CET IMPORT
from .models import *

# ================== CONFIGURATION GLOBALE PREMIUM ==================
admin.site.site_header = format_html('''
    <div style="display: flex; align-items: center; gap: 15px;">
        <span style="font-size: 2.5rem;">📚</span>
        <div>
            <h1 style="margin:0; color: #2c3e50;">SUPNUM ACADEMY</h1>
            <p style="margin:0; color: #7f8c8d;">Plateforme de Gestion Pédagogique</p>
        </div>
    </div>
''')
admin.site.site_title = "SUPNUM Admin"
admin.site.index_title = format_html('<h2 style="color: #34495e;">📊 Tableau de Bord Stratégique</h2>')

# ================== DASHBOARD PERSONNALISÉ ==================
class DashboardAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        
        # Ajouter des statistiques globales
        app_list.insert(0, {
            'name': '📈 VUE D\'ENSEMBLE',
            'app_label': 'dashboard',
            'models': [{
                'name': 'Statistiques Globales',
                'object_name': 'dashboard',
                'admin_url': '/admin/dashboard/',
                'view_only': True,
            }]
        })
        return app_list
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
            path('api/stats/', self.admin_view(self.stats_api), name='stats_api'),
        ]
        return custom_urls + urls
    
    def stats_api(self, request):
        """API pour les graphiques en temps réel"""
        data = {
            'universities': University.objects.count(),
            'specialities': Speciality.objects.count(),
            'levels': Level.objects.count(),
            'semesters': Semester.objects.count(),
            'matieres': Matiere.objects.count(),
            'documents': Document.objects.count(),
            'users': UserProfile.objects.count(),
            
            'documents_by_type': dict(
                Document.objects.values('document_type')
                .annotate(count=Count('id'))
                .values_list('document_type', 'count')
            ),
            
            'levels_distribution': dict(
                Level.objects.values('name')
                .annotate(count=Count('speciality'))
                .values_list('name', 'count')
            ),
        }
        return JsonResponse(data)
    
    def dashboard_view(self, request):
        """Vue du dashboard géant"""
        context = {
            'title': 'Dashboard Stratégique',
            'now': timezone.now(),
            'stats': {
                'universities': University.objects.count(),
                'specialities': Speciality.objects.count(),
                'levels': Level.objects.count(),
                'semesters': Semester.objects.count(),
                'matieres': Matiere.objects.count(),
                'documents': Document.objects.count(),
                'users': UserProfile.objects.count(),
                'alerts': Alert.objects.count(),
                'alerts_unread': AlertReadStatus.objects.filter(is_read=False).count(),
                'alerts_urgent': Alert.objects.filter(priority='urgent').count(),
                'total_downloads': Document.objects.aggregate(total=Sum('download_count'))['total'] or 0,
                'favorites': FavoriteDocument.objects.count(),
            },
            'recent_docs': Document.objects.order_by('-created_at')[:15],
            'popular_docs': Document.objects.order_by('-download_count')[:10],
            'alerts': Alert.objects.filter(is_global=True)[:5],
        }
        return TemplateResponse(request, 'admin/custom_dashboard.html', context)

# ================== SITE ADMIN PERSONNALISÉ ==================
admin_site = DashboardAdminSite(name='myadmin')

# ================== UNIVERSITÉS PREMIUM ==================
@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    list_display = [
        'display_avatar', 
        'colored_name', 
        'stats_cards', 
        'progress_bar',
        'last_activity'
    ]
    list_display_links = ['colored_name']
    search_fields = ['name']
    list_filter = ['created_at']
    list_per_page = 10
    
    fieldsets = (
        ('🏛️ IDENTITÉ', {
            'fields': ('name', 'logo_url', 'description'),
            'classes': ('wide',)
        }),
        ('🔗 RESSOURCES', {
            'fields': ('calendar_url',),
        }),
        ('⏱️ MÉTADONNÉES', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ['created_at', 'updated_at']
    
    def display_avatar(self, obj):
        if obj.logo_url:
            return format_html(
                '<div style="width: 50px; height: 50px; border-radius: 12px; overflow: hidden; border: 2px solid #3498db;">'
                '<img src="{}" style="width:100%; height:100%; object-fit:cover;" />'
                '</div>',
                obj.logo_url
            )
        return format_html('<div style="width:50px;height:50px;border-radius:12px;background:#ecf0f1;display:flex;align-items:center;justify-content:center;">🏛️</div>')
    display_avatar.short_description = ''
    
    def colored_name(self, obj):
        return format_html(
            '<span style="font-weight: bold; font-size: 1.1rem; color: #2c3e50;">{}</span><br>'
            '<small style="color: #7f8c8d;">Créé le {}</small>',
            obj.name, obj.created_at.strftime('%d/%m/%Y')
        )
    colored_name.short_description = 'Université'
    
    def stats_cards(self, obj):
        specialities = obj.specialities.count()
        levels = Level.objects.filter(speciality__university=obj).count()
        docs = Document.objects.filter(matiere__semester__level__speciality__university=obj).count()
        
        return format_html('''
            <div style="display: flex; gap: 10px;">
                <div style="background: #e8f4fd; padding: 8px 12px; border-radius: 8px; text-align: center; min-width: 60px;">
                    <div style="font-size: 1.3rem; font-weight: bold; color: #2980b9;">{}</div>
                    <div style="font-size: 0.7rem; color: #7f8c8d;">Spécialités</div>
                </div>
                <div style="background: #e8f8f0; padding: 8px 12px; border-radius: 8px; text-align: center; min-width: 60px;">
                    <div style="font-size: 1.3rem; font-weight: bold; color: #27ae60;">{}</div>
                    <div style="font-size: 0.7rem; color: #7f8c8d;">Niveaux</div>
                </div>
                <div style="background: #fef5e7; padding: 8px 12px; border-radius: 8px; text-align: center; min-width: 60px;">
                    <div style="font-size: 1.3rem; font-weight: bold; color: #e67e22;">{}</div>
                    <div style="font-size: 0.7rem; color: #7f8c8d;">Documents</div>
                </div>
            </div>
        ''', specialities, levels, docs)
    stats_cards.short_description = 'Statistiques'
    
    def progress_bar(self, obj):
        total_docs = Document.objects.filter(
            matiere__semester__level__speciality__university=obj
        ).count()
        max_docs = 100  # Objectif
        percentage = min(int((total_docs / max_docs) * 100), 100)
        
        color = '#27ae60' if percentage > 70 else '#f39c12' if percentage > 30 else '#e74c3c'
        
        return format_html('''
            <div style="min-width: 150px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="font-size: 0.8rem;">Remplissage</span>
                    <span style="font-weight: bold; color: {};">{}%</span>
                </div>
                <div style="background: #ecf0f1; height: 8px; border-radius: 4px;">
                    <div style="background: {}; width: {}%; height: 8px; border-radius: 4px;"></div>
                </div>
            </div>
        ''', color, percentage, color, percentage)
    progress_bar.short_description = 'Progression'
    
    def last_activity(self, obj):
        last_doc = Document.objects.filter(
            matiere__semester__level__speciality__university=obj
        ).order_by('-created_at').first()
        
        if last_doc:
            return format_html(
                '<span style="color: #2ecc71;">●</span> {}<br><small>{}</small>',
                last_doc.created_at.strftime('%H:%M'),
                last_doc.title[:20]
            )
        return format_html('<span style="color: #95a5a6;">● Aucune activité</span>')
    last_activity.short_description = 'Dernière activité'

# ================== DOCUMENTS PREMIUM ==================
@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = [
        'preview_icon',
        'colored_title',
        'document_badge',
        'file_badge',
        'stats_display',
        'actions_buttons'
    ]
    list_display_links = ['colored_title']
    list_filter = ['document_type', 'file_type', 'is_published', 'created_at']
    search_fields = ['title', 'description']
    list_per_page = 20
    
    fieldsets = (
        ('📄 DOCUMENT', {
            'fields': ('matiere', 'title', 'description', 'file'),
            'classes': ('wide',)
        }),
        ('🏷️ CLASSIFICATION', {
            'fields': ('document_type', 'file_type'),
        }),
        ('📊 MÉTRIQUES', {
            'fields': ('is_published', 'download_count'),
        }),
        ('⏱️ MÉTADONNÉES', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )
    readonly_fields = ['download_count', 'created_at', 'updated_at']
    
    def preview_icon(self, obj):
        icons = {
            'CM': '📚', 'TD': '✏️', 'TP': '🔬', 
            'EXAM': '📝', 'PROJET': '🎯', 'AUTRE': '📁'
        }
        colors = {
            'CM': '#3498db', 'TD': '#2ecc71', 'TP': '#e74c3c',
            'EXAM': '#f39c12', 'PROJET': '#9b59b6', 'AUTRE': '#95a5a6'
        }
        icon = icons.get(obj.document_type, '📄')
        color = colors.get(obj.document_type, '#34495e')
        
        return format_html(
            '<div style="width: 40px; height: 40px; background: {}20; border-radius: 10px; '
            'display: flex; align-items: center; justify-content: center; font-size: 1.5rem;">'
            '{}</div>',
            color, icon
        )
    preview_icon.short_description = ''
    
    def colored_title(self, obj):
        return format_html(
            '<span style="font-weight: bold; color: #2c3e50;">{}</span><br>'
            '<small style="color: #7f8c8d;">{}</small>',
            obj.title[:50] + ('...' if len(obj.title) > 50 else ''),
            obj.matiere.name[:30]
        )
    colored_title.short_description = 'Titre'
    
    def document_badge(self, obj):
        badges = {
            'CM': ('Cours Magistral', '#3498db'),
            'TD': ('Travaux Dirigés', '#2ecc71'),
            'TP': ('Travaux Pratiques', '#e74c3c'),
            'EXAM': ('Examen', '#f39c12'),
            'PROJET': ('Projet', '#9b59b6'),
        }
        name, color = badges.get(obj.document_type, ('Document', '#95a5a6'))
        
        return format_html(
            '<span style="background: {}20; color: {}; padding: 5px 10px; border-radius: 20px; '
            'font-size: 0.8rem; font-weight: 500;">{}</span>',
            color, color, name
        )
    document_badge.short_description = 'Type'
    
    def file_badge(self, obj):
        icons = {'pdf': '📕', 'ppt': '📊', 'doc': '📘', 'video': '🎥', 'other': '📄'}
        colors = {'pdf': '#e74c3c', 'ppt': '#f39c12', 'doc': '#3498db', 'video': '#9b59b6', 'other': '#95a5a6'}
        
        icon = icons.get(obj.file_type, '📄')
        color = colors.get(obj.file_type, '#34495e')
        
        return format_html(
            '<span style="color: {};">{} {}</span>',
            color, icon, obj.file_type.upper()
        )
    file_badge.short_description = 'Format'
    
    def stats_display(self, obj):
        return format_html('''
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="text-align: center;">
                    <span style="font-weight: bold; color: #2c3e50;">{}</span>
                    <div style="font-size: 0.7rem; color: #7f8c8d;">⬇️ Téléch.</div>
                </div>
                <div style="text-align: center;">
                    <span style="font-weight: bold; color: #2c3e50;">{}</span>
                    <div style="font-size: 0.7rem; color: #7f8c8d;">⭐ Favoris</div>
                </div>
            </div>
        ''', obj.download_count, obj.favorites.count())
    stats_display.short_description = 'Stats'
    
    def actions_buttons(self, obj):
        return format_html('''
            <div style="display: flex; gap: 5px;">
                <a href="{}" target="_blank" style="background: #3498db; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none; font-size: 0.8rem;">👁️ Voir</a>
                <a href="{}" style="background: #27ae60; color: white; padding: 5px 10px; border-radius: 5px; text-decoration: none; font-size: 0.8rem;">✏️ Éditer</a>
            </div>
        ''', obj.file.url if obj.file else '#', reverse('admin:python_project_document_change', args=[obj.id]))
    actions_buttons.short_description = 'Actions'

# ================== AUTRES MODÈLES ==================
@admin.register(Speciality)
class SpecialityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'university', 'code']
    list_filter = ['university']
    search_fields = ['name', 'code']

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'speciality', 'order']
    list_filter = ['speciality__university', 'name']
    search_fields = ['speciality__name']

@admin.register(Semester)
class SemesterAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'code', 'level', 'order']
    list_filter = ['level__speciality__university']

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'semester', 'credits', 'coefficient']
    list_filter = ['semester__level__speciality__university']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'priority', 'is_global', 'created_at']
    list_filter = ['priority', 'is_global']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'email', 'first_name', 'last_name', 'university']
    search_fields = ['email', 'first_name', 'last_name']

@admin.register(FavoriteDocument)
class FavoriteDocumentAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'document', 'created_at']

@admin.register(AlertReadStatus)
class AlertReadStatusAdmin(admin.ModelAdmin):
    list_display = ['alert', 'user_id', 'is_read', 'read_at']

@admin.register(UserUniversity)
class UserUniversityAdmin(admin.ModelAdmin):
    list_display = ['user_id', 'university', 'created_at']