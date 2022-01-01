from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.http import request
from parcinfo.models import Parc
from .models import Machine
from .forms import MachineForm, FormMachine
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import geocoder
import folium
##valid_form 
# Create your views here.
# class HomeView():
# 	model = geoclass.m
# 	#ordering = ['date_creation']
# 	template_name = 'home.html'
@login_required(login_url="/login/")
def mapview(request):
	return render(request, 'map.html')
@login_required(login_url="/login/")
def HomeView(request):
	parc = Parc.objects.get(user=request.user)
	location = geocoder.osm(parc.adresse)
	m = folium.Map(location=[parc.alt, parc.long],
	               zoom_start=8)
	folium.Marker([parc.alt, parc.long], tooltip=request.user.username,
	              icon=folium.Icon(color='blue')).add_to(m)
	# for liste in list_parc:
	#     if erreur.objects.filter(nom_parc=liste.name).exists():
	#         folium.Marker([liste.lattitude, liste.longitude], tooltip='parc have a Errors',
	#                       popup=liste.city, icon=folium.Icon(color='orange')).add_to(m)
	#     elif delete_parc.objects.filter(nomparc=liste.name).exists():
	#         folium.Marker([liste.lattitude, liste.longitude], tooltip='Demande of Delete',
	#                       popup=liste.city, icon=folium.Icon(color='red')).add_to(m)
	#     else:
	#         folium.Marker([liste.lattitude, liste.longitude], tooltip='Parc Etat Normale',
	#                       popup=liste.city, icon=folium.Icon(color='green')).add_to(m)
	m.save("/home/aymane/Desktop/mobile/WebApp/webapp/app_mecanisme/templates/map.html")
	m = m._repr_html_()
	context = {'map': m,'parc':parc}
	return render(request, 'home.html', context)
#@login_required(login_url="/login/")
class MachineView(ListView):
	model = Machine
	ordering = ['date_creation'];
	template_name = 'machines-view.html'
	def get_queryset(self):
		return Machine.objects.filter(parc=self.request.user)
#@login_required(login_url="/login/")
class MachineDetailView(DetailView):
	model = Machine
	template_name = 'machine-detail.html'
#@login_required(login_url="/login/")
class MachineCreateView(CreateView):
	model = Machine
	form_class = FormMachine
	template_name = 'machine-add.html'
	def form_valid(self, form):
		p = Parc.objects.get(user=self.request.user)
		p.nbr_machine += 1
		p.save()
		form.instance.parc = self.request.user
		return super(MachineCreateView, self).form_valid(form)
#@login_required(login_url="/login/")
class MachineUpdateView(UpdateView):
	model = Machine
	form_class = MachineForm
	template_name = 'machine-update.html'
	def form_valid(self, form):
		p = Parc.objects.get(user=self.request.user)
		if(form.instance.probleme_ram != ''):
			p.nbr_ram += 1
		if(form.instance.probleme_os != ''):
			p.nbr_os += 1
		if(form.instance.probleme_dd != ''):
			p.nbr_dd += 1
		if(form.instance.probleme_alimentation_affichage != ''):
			p.nbr_af += 1
		if(form.instance.autre_probleme != ''):
			p.nbr_autre += 1
		p.nbr_err = p.nbr_ram+p.nbr_os+p.nbr_dd+p.nbr_af+p.nbr_autre
		p.save()
		return super(MachineUpdateView, self).form_valid(form)
#@login_required(login_url="/login/")
class MachineDeleteView(DeleteView):
	model = Machine
	template_name = 'machine-delete.html'
	success_url = reverse_lazy('machine-view')
	def delete(self, *args, **kwargs):
		print(Machine.objects.all())
		p = Parc.objects.filter(user=self.request.user)
		m = Machine.objects.filter(parc=self.request.user)
		p.nbr_machine -= 1
		if(m.probleme_ram != ''):
			p.nbr_ram -= 1
		if(m.probleme_os != ''):
			p.nbr_os -= 1
		if(m.probleme_dd != ''):
			p.nbr_dd -= 1
		if(m.probleme_alimentation_affichage != ''):
			p.nbr_af -= 1
		if(m.autre_probleme != ''):
			p.nbr_autre -= 1
		p.nbr_err = p.nbr_ram+p.nbr_os+p.nbr_dd+p.nbr_af+p.nbr_autre
		p.save()
		return super(MachineDeleteView, self).delete(*args, **kwargs)
@login_required(login_url="/login/")
def RedirectView(request):
	if(request.user.is_authenticated):
		response = redirect('/home')
	else:
		response = redirect("/login")
	return response
@login_required(login_url="/login/")
def suppresion(request):
	if request.method == 'POST':
		p = Parc.objects.get(user=request.user)
		p.demande_s = True
		p.save()
		return HttpResponseRedirect('/home')
	return render(request, "suppresion.html", {'nom':request.user.username})