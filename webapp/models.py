from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Member(User):
    """Class Member."""
    phone = models.CharField(max_length=20)
    birthday = models.DateField()
    address = models.CharField(max_length=100)
    SUIT_CHOICES = {
        ('TENOR', 'Tenor'),
        ('ALTO', 'Alto'),
        ('BAIXO', 'Baixo'),
        ('SOPRANO', 'Soprano'),
        ('BARITONO', 'Baritono'),
    }
    suit = models.CharField(
        max_length=20,
        choices=SUIT_CHOICES,
        default='TENOR'
    )
    #terms_agreed = models.BooleanField(default=False)
    created_at = models.DateField()

    def __str__(self) -> str:
        return f'{self.username} - {self.suit}'
    
    class Meta:
        verbose_name = "Membro"
        verbose_name_plural = "Membros"

class Event(models.Model):
    """Class Event."""
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=100)
    date = models.DateField()
    location = models.CharField(max_length=100)
    updated_at = models.DateField()

    def __str__(self) -> str:
        return self.name
    
class Notice(models.Model):
    """Class Notice."""
    description = models.CharField(max_length=100)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    created_at = models.DateField()

    def __str__(self) -> str:
        return self.title


class Music(models.Model):
    """Class Music."""
    name = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    cover = models.ImageField(upload_to='covers/', blank=True, null=True)
    year = models.DateField()
    letter = models.TextField()
    created_at = models.DateField()
    members = models.ManyToManyField(Member, through='MusicMember')

    def __str__(self) -> str:
        return self.name


class MusicMember(models.Model):
    """Class MusicMember."""
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    favorited = models.BooleanField(default=False)
    hits = models.IntegerField(default=0)
    class Meta:
        unique_together = ('member', 'music')


    def __str__(self) -> str:
        return self.member.username + ' - ' + self.music.name
    
class File(models.Model):
    """Class File."""
    name = models.CharField(max_length=30)
    #file = models.FileField(upload_to='files/')
    url = models.CharField(max_length=150, blank=True, null=True)
    created_at = models.DateField()
    music = models.ForeignKey(Music, on_delete=models.CASCADE)
    TYPE_CHOICES = {
        ('audio', 'Audio'),
        ('partitura', 'Partitura'),
        ('letra', 'Letra'),
        ('cifra', 'Cifra'),
    }
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='TENOR'
    )

    def __str__(self) -> str:
        return self.name
    
