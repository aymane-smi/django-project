from django.db import models
from django.urls import reverse
from datetime import datetime, date
from django.contrib.auth.models import User
# Create your models here.
class Machine(models.Model):
	nom                             = models.TextField(max_length=30)
	probleme_ram                    = models.TextField(max_length=200, blank=True)
	probleme_os                     = models.TextField(max_length=200, blank=True)
	probleme_dd                     = models.TextField(max_length=200, blank=True)
	probleme_alimentation_affichage = models.TextField(max_length=200, blank=True)
	autre_probleme                  = models.TextField(blank=True)
	date_creation                   = models.DateField(auto_now_add=True)
	parc                            = models.ForeignKey(User, on_delete=models.CASCADE)
	def __str__(self):
		return self.nom+'|'+str(self.id)
	def get_absolute_url(self):
		return reverse('home')
# class Parc(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     nbr_machine = models.IntegerField(default=0)
#     nbr_err = models.IntegerField(default=0)
#     demande_s = models.BooleanField(default=False)
#     nbr_ram = models.IntegerField(default=0)
#     nbr_dd = models.IntegerField(default=0)
#     nbr_os = models.IntegerField(default=0)
#     nbr_af = models.IntegerField(default=0)
#     adresse = models.CharField(blank=True, max_length=400)
#     nbr_autre = models.IntegerField(default=0)
#     alt = models.FloatField(default=0)
#     long = models.FloatField(default=0)