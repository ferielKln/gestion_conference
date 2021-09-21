from django.db import models
from datetime import datetime


# Create your models here.
class conference(models.Model):
    Intenationale='Internationale'
    Nationale='Nationale'
    audience_choices={
        (Intenationale,'Internationale'),
        (Nationale,'Nationale'),
    }
    nom = models.CharField(max_length=1000,unique=True)
    chair=models.CharField(max_length=1000)
    organisateur=models.CharField(max_length=1000)
    label =models.CharField(max_length=1000,blank=True,null=True)
    audience=models.CharField(max_length=15,choices=audience_choices)
    date=models.DateField()
    lieu=models.CharField(max_length=1000)
    description=models.TextField()

    def __str__(self):
        return self.nom 
    class Meta:
        verbose_name='Conférence'
        verbose_name_plural='Conférences'



class MotCle(models.Model):
    mot = models.CharField(max_length=1000,unique=True)

    def __str__(self):
        return self.mot 
        

class Auteur(models.Model):
    nom = models.CharField(max_length=1000)
    prenom=models.CharField(max_length=1000)

    def __str__(self):
        return self.nom +" "+ self.prenom


class article(models.Model):
    titre=models.CharField(max_length=1000)
    auteurs = models.ManyToManyField(Auteur)
    langue= models.CharField(max_length=1000)
    motsClé = models.ManyToManyField(MotCle)
    conférence=models.ForeignKey(conference, on_delete=models.CASCADE, related_name='Articles')
    résumé=models.TextField()
    date_publication = models.DateField(auto_now_add=True)
    fichier=models.FileField(upload_to='media')

    def __str__(self):
        return self.titre
    class Meta:
        verbose_name='Article'
        verbose_name_plural='Articles' 


class Visitor_Infos(models.Model):
    ip_address = models.GenericIPAddressField()
    page_visited = models.TextField()
    event_date = models.DateTimeField(default=datetime.now)