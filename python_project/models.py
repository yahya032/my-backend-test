from django.db import models
from django.utils import timezone

class University(models.Model):
    """Modèle pour les universités"""
    name = models.CharField(max_length=200, verbose_name="Nom de l'université")
    logo_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Logo URL")
    calendar_url = models.URLField(max_length=500, blank=True, null=True, verbose_name="Calendrier URL")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    
    class Meta:
        verbose_name = "Université"
        verbose_name_plural = "Universités"
        ordering = ['name']
        indexes = [models.Index(fields=['name'])]
    
    def __str__(self):
        return self.name


class Speciality(models.Model):
    """Modèle pour les spécialités"""
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='specialities')
    name = models.CharField(max_length=200, verbose_name="Nom de la spécialité")
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Code")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    
    class Meta:
        verbose_name = "Spécialité"
        verbose_name_plural = "Spécialités"
        ordering = ['university__name', 'name']
        unique_together = ['university', 'name']
        indexes = [models.Index(fields=['university', 'name'])]
    
    def __str__(self):
        return f"{self.name} - {self.university.name}"


class Level(models.Model):
    """Modèle pour les niveaux (L1, L2, L3, M1, M2)"""
    LEVEL_CHOICES = [
        ('L1', 'Licence 1'),
        ('L2', 'Licence 2'),
        ('L3', 'Licence 3'),
        ('M1', 'Master 1'),
        ('M2', 'Master 2'),
    ]
    
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, related_name='levels')
    name = models.CharField(max_length=10, choices=LEVEL_CHOICES, verbose_name="Niveau")
    code = models.CharField(max_length=20, blank=True, null=True, verbose_name="Code interne")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    order = models.IntegerField(default=0, verbose_name="Ordre d'affichage")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Niveau"
        verbose_name_plural = "Niveaux"
        ordering = ['order', 'name']
        unique_together = ['speciality', 'name']
        indexes = [models.Index(fields=['speciality', 'order'])]
    
    def __str__(self):
        return f"{self.get_name_display()} - {self.speciality.name}"


class Semester(models.Model):
    """Modèle pour les semestres"""
    level = models.ForeignKey(Level, on_delete=models.CASCADE, related_name='semesters')
    name = models.CharField(max_length=100, verbose_name="Nom du semestre")
    code = models.CharField(max_length=20, verbose_name="Code (S1, S2, etc.)")
    order = models.IntegerField(default=0, verbose_name="Ordre")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Semestre"
        verbose_name_plural = "Semestres"
        ordering = ['level__order', 'order']
        unique_together = ['level', 'code']
        indexes = [models.Index(fields=['level', 'order'])]
    
    def __str__(self):
        return f"{self.name} - {self.level}"


class Matiere(models.Model):
    """Modèle pour les matières"""
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, related_name='matieres')
    name = models.CharField(max_length=200, verbose_name="Nom de la matière")
    code = models.CharField(max_length=50, blank=True, null=True, verbose_name="Code")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    credits = models.IntegerField(default=0, verbose_name="Crédits")
    coefficient = models.FloatField(default=1.0, verbose_name="Coefficient")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    
    class Meta:
        verbose_name = "Matière"
        verbose_name_plural = "Matières"
        ordering = ['semester__level__order', 'semester__order', 'name']
        unique_together = ['semester', 'name']
        indexes = [models.Index(fields=['semester', 'name'])]
    
    def __str__(self):
        return f"{self.name} - {self.semester}"


class Document(models.Model):
    """Modèle pour les documents (PDF, PPT, etc.)"""
    TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('ppt', 'PowerPoint'),
        ('doc', 'Word'),
        ('video', 'Vidéo'),
        ('other', 'Autre'),
    ]
    
    # Type de document pédagogique
    DOCUMENT_TYPE_CHOICES = [
        ('CM', 'Cours Magistral'),
        ('TD', 'Travaux Dirigés'),
        ('TP', 'Travaux Pratiques'),
        ('EXAM', 'Examen'),
        ('PROJET', 'Projet'),
        ('AUTRE', 'Autre'),
    ]
    
    matiere = models.ForeignKey(Matiere, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=300, verbose_name="Titre du document")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    file = models.FileField(upload_to='documents/%Y/%m/%d/', verbose_name="Fichier")
    file_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='pdf', verbose_name="Type de fichier")
    document_type = models.CharField(  # NOUVEAU CHAMP
        max_length=10, 
        choices=DOCUMENT_TYPE_CHOICES, 
        default='CM',
        verbose_name="Type de document"
    )
    is_published = models.BooleanField(default=True, verbose_name="Publié")
    download_count = models.IntegerField(default=0, verbose_name="Nombre de téléchargements")
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    
    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['matiere', '-created_at']),
            models.Index(fields=['file_type']),
            models.Index(fields=['document_type']),  # NOUVEL INDEX
            models.Index(fields=['is_published']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Déterminer automatiquement le type de fichier
        if self.file:
            ext = self.file.name.split('.')[-1].lower()
            type_map = {
                'pdf': 'pdf',
                'ppt': 'ppt', 'pptx': 'ppt',
                'doc': 'doc', 'docx': 'doc',
                'mp4': 'video', 'avi': 'video', 'mov': 'video',
            }
            self.file_type = type_map.get(ext, 'other')
        
        # NOUVEAU : Déterminer automatiquement le type de document à partir du titre
        if self.title:
            title_lower = self.title.lower()
            if 'td' in title_lower or 't.d' in title_lower or 'td1' in title_lower or 'td2' in title_lower:
                self.document_type = 'TD'
            elif 'tp' in title_lower or 't.p' in title_lower or 'tp1' in title_lower or 'tp2' in title_lower:
                self.document_type = 'TP'
            elif 'examen' in title_lower or 'exam' in title_lower or 'ds' in title_lower or 'controle' in title_lower:
                self.document_type = 'EXAM'
            elif 'projet' in title_lower:
                self.document_type = 'PROJET'
            elif 'cours' in title_lower or 'cm' in title_lower or 'chapitre' in title_lower or 'chap' in title_lower:
                self.document_type = 'CM'
            # Sinon, garder la valeur par défaut (CM)
        
        super().save(*args, **kwargs)


class FavoriteDocument(models.Model):
    """Modèle pour les documents favoris des utilisateurs"""
    user_id = models.CharField(max_length=255, verbose_name="ID Firebase User", db_index=True)
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name='favorites')
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Document favori"
        verbose_name_plural = "Documents favoris"
        unique_together = ['user_id', 'document']
        indexes = [
            models.Index(fields=['user_id', '-created_at']),
        ]
    
    def __str__(self):
        return f"{self.user_id} - {self.document.title}"


class Alert(models.Model):
    """Modèle pour les alertes/notifications"""
    PRIORITY_CHOICES = [
        ('low', 'Basse'),
        ('medium', 'Moyenne'),
        ('high', 'Haute'),
        ('urgent', 'Urgente'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titre")
    message = models.TextField(verbose_name="Message")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    is_global = models.BooleanField(default=False, verbose_name="Alerte globale")
    user_id = models.CharField(max_length=255, blank=True, null=True, verbose_name="ID Utilisateur cible", db_index=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, blank=True, null=True, related_name='alerts')
    speciality = models.ForeignKey(Speciality, on_delete=models.CASCADE, blank=True, null=True, related_name='alerts')
    level = models.ForeignKey(Level, on_delete=models.CASCADE, blank=True, null=True, related_name='alerts')
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    expires_at = models.DateTimeField(blank=True, null=True, verbose_name="Date d'expiration")
    
    class Meta:
        verbose_name = "Alerte"
        verbose_name_plural = "Alertes"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['user_id', '-created_at']),
            models.Index(fields=['is_global']),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def is_expired(self):
        """Vérifie si l'alerte est expirée"""
        if self.expires_at:
            return timezone.now() > self.expires_at
        return False


class AlertReadStatus(models.Model):
    """Suivi des alertes lues par utilisateur"""
    alert = models.ForeignKey(Alert, on_delete=models.CASCADE, related_name='read_statuses')
    user_id = models.CharField(max_length=255, verbose_name="ID Firebase User", db_index=True)
    is_read = models.BooleanField(default=False, verbose_name="Lue")
    read_at = models.DateTimeField(blank=True, null=True, verbose_name="Lu le")
    
    class Meta:
        verbose_name = "Statut de lecture"
        verbose_name_plural = "Statuts de lecture"
        unique_together = ['alert', 'user_id']
        indexes = [models.Index(fields=['user_id', 'is_read'])]
    
    def __str__(self):
        return f"{self.user_id} - {self.alert.title}: {'Lu' if self.is_read else 'Non lu'}"
    
    def save(self, *args, **kwargs):
        if self.is_read and not self.read_at:
            self.read_at = timezone.now()
        super().save(*args, **kwargs)


class UserProfile(models.Model):
    """Profil utilisateur étendu"""
    user_id = models.CharField(max_length=255, unique=True, verbose_name="ID Firebase User", db_index=True)
    email = models.EmailField(verbose_name="Email")
    first_name = models.CharField(max_length=100, verbose_name="Prénom")
    last_name = models.CharField(max_length=100, verbose_name="Nom")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    photo_url = models.URLField(blank=True, null=True, verbose_name="Photo URL")
    university = models.ForeignKey(University, on_delete=models.SET_NULL, blank=True, null=True)
    speciality = models.ForeignKey(Speciality, on_delete=models.SET_NULL, blank=True, null=True)
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Dernière mise à jour")
    
    class Meta:
        verbose_name = "Profil utilisateur"
        verbose_name_plural = "Profils utilisateurs"
        indexes = [models.Index(fields=['user_id'])]
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()


class UserUniversity(models.Model):
    """
    Lie les utilisateurs Firebase aux universités pour les notifications
    """
    user_id = models.CharField(max_length=255, verbose_name="ID Firebase User", db_index=True)
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='user_universities')
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Date de création")

    class Meta:
        verbose_name = "Utilisateur Université"
        verbose_name_plural = "Utilisateurs Universités"
        unique_together = ['user_id', 'university']
        indexes = [
            models.Index(fields=['user_id']),
            models.Index(fields=['university']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_id} - {self.university.name}"