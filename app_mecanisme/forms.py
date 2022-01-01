from django import forms
from .models import Machine
class MachineForm(forms.ModelForm):
	class Meta:
		model = Machine
		fields = ('nom', 'probleme_os', 'probleme_ram', 'probleme_dd', 'probleme_alimentation_affichage', 'autre_probleme')#specific fields
		widgets = {
		'nom': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'nom de la machine'}),
		'probleme_ram': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'les problèmes de la RAM'}),
		'probleme_os': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "les problèmes de le système d'exploitation"}),
		'probleme_dd': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "les problèmes de concernent le disque dur"}),
		'probleme_alimentation_affichage': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "les problèmes de l'alimentation et d'affichage"}),
		'autre_probleme': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'autres problèmes'})
		}
class FormMachine(forms.ModelForm):
	class Meta:
		model = Machine
		fields = ('nom',)
		widgets = {
		'nom': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'nom de la machine'})
		}