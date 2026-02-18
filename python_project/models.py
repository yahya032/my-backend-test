from django.db import models
from django.contrib.auth.models import User

# ---------------- ALERT ----------------
class Alert(models.Model):
    user_id = models.CharField(max_length=255)  # UID Firebase
    title = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.user_id})"


# ---------------- UNIVERSITY ----------------
class University(models.Model):
    name = models.CharField(max_length=200, unique=True)
    logo = models.ImageField(upload_to='universities/', blank=True, null=True)
    calendar = models.FileField(upload_to='calendars/', blank=True, null=True)  # PDF calendrier

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_calendar_url(self):
        if self.calendar:
            return self.calendar.url
        return None

    def get_logo_url(self):
        if self.logo:
            return self.logo.url
        return None


# ---------------- SPECIALITY ----------------
class Speciality(models.Model):
    university = models.ForeignKey(
        University,
        on_delete=models.PROTECT,
        related_name='specialities'
    )
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "specialities"
        unique_together = ('university', 'name')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} - {self.university.name}"


# ---------------- LEVEL ----------------
class Level(models.Model):
    name = models.CharField(max_length=10, unique=True)  # Ex: L1, L2, L3, M1, M2

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


# ---------------- SEMESTER ----------------
class Semester(models.Model):
    name = models.CharField(max_length=10)  # Ex: S1, S2
    level = models.ForeignKey(
        Level,
        on_delete=models.PROTECT,
        related_name='semesters'
    )

    class Meta:
        unique_together = ('level', 'name')
        ordering = ['level__name', 'name']

    def __str__(self):
        return f"{self.level.name} - {self.name}"


# ---------------- MATIERE ----------------
class Matiere(models.Model):
    name = models.CharField(max_length=100)
    semester = models.ForeignKey(
        Semester,
        on_delete=models.PROTECT,
        related_name='matieres'
    )
    speciality = models.ForeignKey(
        Speciality,
        on_delete=models.PROTECT,
        related_name='matieres'
    )
    level = models.ForeignKey(            
        Level,
        on_delete=models.PROTECT,
        related_name='matieres',
        blank=True,
        null=True
    )

    class Meta:
        unique_together = ('semester', 'name', 'speciality')
        ordering = ['semester__level__name', 'semester__name', 'name']

    def save(self, *args, **kwargs):
        if not self.level and self.semester:
            self.level = self.semester.level
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.semester})"


# ---------------- DOCUMENT ----------------
class Document(models.Model):
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='documents/')
    matiere = models.ForeignKey(
        Matiere,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='documents'
    )

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_file_url(self):
        if self.file:
            return self.file.url
        return None


# ---------------- USER-UNIVERSITY RELATION ----------------
class UserUniversity(models.Model):
    """
    Lie les utilisateurs Firebase aux universités pour les notifications
    """
    user_id = models.CharField(max_length=255)  # UID Firebase
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user_id', 'university')
        verbose_name_plural = "User universities"

    def __str__(self):
        return f"{self.user_id} - {self.university.name}"