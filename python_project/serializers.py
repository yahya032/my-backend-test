from rest_framework import serializers
from .models import *

class UniversitySerializer(serializers.ModelSerializer):
    """Sérialiseur pour les universités"""
    class Meta:
        model = University
        fields = ['id', 'name', 'description', 'logo_url', 'calendar_url', 'created_at', 'updated_at']


class SpecialitySerializer(serializers.ModelSerializer):
    """Sérialiseur pour les spécialités"""
    university_name = serializers.CharField(source='university.name', read_only=True)
    
    class Meta:
        model = Speciality
        fields = ['id', 'name', 'code', 'description', 'university', 'university_name', 'created_at', 'updated_at']


class LevelSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les niveaux"""
    speciality_name = serializers.CharField(source='speciality.name', read_only=True)
    
    class Meta:
        model = Level
        fields = ['id', 'name', 'code', 'description', 'order', 'speciality', 'speciality_name', 'created_at']


class SemesterSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les semestres"""
    level_name = serializers.CharField(source='level.name', read_only=True)
    
    class Meta:
        model = Semester
        # ✅ AJOUT du champ 'description' (nouveau dans models.py)
        fields = ['id', 'name', 'description', 'code', 'order', 'level', 'level_name', 'created_at']


class MatiereSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les matières"""
    semester_name = serializers.CharField(source='semester.name', read_only=True)
    
    class Meta:
        model = Matiere
        fields = ['id', 'name', 'code', 'description', 'credits', 'coefficient', 'semester', 'semester_name', 'created_at', 'updated_at']


class DocumentSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les documents"""
    matiere_name = serializers.CharField(source='matiere.name', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = [
            'id', 
            'title', 
            'description', 
            'file', 
            'file_url', 
            'file_type', 
            'document_type',
            'is_published', 
            'download_count', 
            'matiere', 
            'matiere_name', 
            'created_at', 
            'updated_at'
        ]
    
    def get_file_url(self, obj):
        """Génère l'URL complète du fichier"""
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class AlertSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les alertes"""
    class Meta:
        model = Alert
        fields = '__all__'


class AlertReadStatusSerializer(serializers.ModelSerializer):
    """Sérialiseur pour le statut de lecture des alertes"""
    alert_title = serializers.CharField(source='alert.title', read_only=True)
    
    class Meta:
        model = AlertReadStatus
        fields = ['id', 'alert', 'alert_title', 'user_id', 'is_read', 'read_at']


class FavoriteDocumentSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les documents favoris"""
    document_details = DocumentSerializer(source='document', read_only=True)
    document_title = serializers.CharField(source='document.title', read_only=True)
    
    class Meta:
        model = FavoriteDocument
        fields = ['id', 'user_id', 'document', 'document_title', 'document_details', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    """Sérialiseur pour les profils utilisateur"""
    full_name = serializers.CharField(source='full_name', read_only=True)
    university_name = serializers.CharField(source='university.name', read_only=True, allow_null=True)
    speciality_name = serializers.CharField(source='speciality.name', read_only=True, allow_null=True)
    level_name = serializers.CharField(source='level.name', read_only=True, allow_null=True)
    
    class Meta:
        model = UserProfile
        fields = [
            'id', 
            'user_id', 
            'email', 
            'first_name', 
            'last_name', 
            'full_name',
            'phone', 
            'photo_url',
            'university', 
            'university_name',
            'speciality', 
            'speciality_name',
            'level', 
            'level_name',
            'created_at', 
            'updated_at'
        ]