# serializers.py
from rest_framework import serializers
from .models import *

class UniversitySerializer(serializers.ModelSerializer):
    class Meta:
        model = University
        fields = '__all__'


class SpecialitySerializer(serializers.ModelSerializer):
    university_name = serializers.CharField(source='university.name', read_only=True)
    
    class Meta:
        model = Speciality
        fields = ['id', 'name', 'code', 'description', 'university', 'university_name', 'created_at']


class LevelSerializer(serializers.ModelSerializer):
    speciality_name = serializers.CharField(source='speciality.name', read_only=True)
    
    class Meta:
        model = Level
        fields = ['id', 'name', 'code', 'description', 'order', 'speciality', 'speciality_name']


class SemesterSerializer(serializers.ModelSerializer):
    level_name = serializers.CharField(source='level.name', read_only=True)
    
    class Meta:
        model = Semester
        fields = ['id', 'name', 'code', 'order', 'level', 'level_name']


class MatiereSerializer(serializers.ModelSerializer):
    semester_name = serializers.CharField(source='semester.name', read_only=True)
    
    class Meta:
        model = Matiere
        fields = ['id', 'name', 'code', 'description', 'credits', 'coefficient', 'semester', 'semester_name']


class DocumentSerializer(serializers.ModelSerializer):
    matiere_name = serializers.CharField(source='matiere.name', read_only=True)
    file_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Document
        fields = ['id', 'title', 'description', 'file', 'file_url', 'file_type', 
                  'is_published', 'download_count', 'matiere', 'matiere_name', 'created_at']
    
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and request:
            return request.build_absolute_uri(obj.file.url)
        return None


class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields = '__all__'


class AlertReadStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertReadStatus
        fields = '__all__'


class FavoriteDocumentSerializer(serializers.ModelSerializer):
    document_details = DocumentSerializer(source='document', read_only=True)
    
    class Meta:
        model = FavoriteDocument
        fields = ['id', 'user_id', 'document', 'document_details', 'created_at']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'