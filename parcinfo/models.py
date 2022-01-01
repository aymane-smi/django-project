from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.


class Parc(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="admin")
    nom_parc = models.CharField(blank=True, max_length=400)
    nbr_machine = models.IntegerField(default=0)
    nbr_err = models.IntegerField(default=0)
    demande_s = models.BooleanField(default=False)
    nbr_ram = models.IntegerField(default=0)
    nbr_dd = models.IntegerField(default=0)
    nbr_os = models.IntegerField(default=0)
    nbr_af = models.IntegerField(default=0)
    adresse = models.CharField(blank=True, max_length=400)
    nbr_autre = models.IntegerField(default=0)
    alt = models.FloatField(default=0)
    long = models.FloatField(default=0)

    def __str__(self):
        return self.user.username


# class Machine(models.Model):
#     nom = models.TextField(max_length=30)
#     probleme_ram = models.TextField(max_length=200, default=None, blank=True)
#     probleme_os = models.TextField(max_length=200, default=None, blank=True)
#     probleme_dd = models.TextField(max_length=200, default=None, blank=True)
#     probleme_alimentation_affichage = models.TextField(
#         max_length=200, default=None, blank=True)
#     autre_probleme = models.TextField(default=None, blank=True)
#     date_creation = models.DateField(auto_now_add=True)
#     parc = models.ForeignKey(
#         Parc, on_delete=models.CASCADE, related_name="admin")

#     def __str__(self):
#         return self.nom+'|'+str(self.id)
