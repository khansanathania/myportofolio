import uuid
from django.contrib.auth.models import User
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Experience(models.Model):
    EXPERIENCE_CHOICES = [
        ('internship', 'Internship'),
        ('research', 'Research'),
        ('volunteer', 'Volunteer'),
        ('part-time', 'Part-Time'),
        ('full-time', 'Full-Time'),
        ('freelance', 'Freelance'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default='full-time')
    thumbnail = models.URLField(blank=True, null=True)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(blank=True, null=True)
    def __str__(self):
        return self.title
    
    @property
    def is_ongoing(self):
        return self.ended_at is None
    
class Achievement(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    issuer = models.CharField(max_length=255)
    issued_at = models.DateField()
    credential_url = models.URLField(blank = True, default ="")
    starred_by = models.ManyToManyField(
        User, related_name="starred_achievements", blank=True
    )
        # untuk memnetukan tampilan teks
    def __str__(self):
        return f"{self.title} - {self.issuer}"
    
class Skill(models.Model):
        name = models.CharField(max_length=100)
        # Level 1-5, sesuai jumlah titik pada tampilan Skills
        level = models.PositiveSmallIntegerField(
            default=3,
            validators=[MinValueValidator(1), MaxValueValidator(5)],
        )
        # Relasi star dari Tugas 4: satu pengguna maksimal satu star per skill
        starred_by = models.ManyToManyField(
            User, related_name="starred_skills", blank=True
        )
    
        def __str__(self):
            return f"{self.name} ({self.level}/5)"