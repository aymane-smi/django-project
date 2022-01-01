from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.auth import authenticate, login, logout
from .models import Parc
from  app_mecanisme.models import Machine
import folium
import geocoder
from django.contrib.admin.views.decorators import staff_member_required



# Create your views here.

@staff_member_required
def ajoutparc(request):
    if request.method == 'POST':
        username = request.POST.get('usermane')
        email = request.POST.get('email')
        passing = request.POST.get('password')
        prenom = request.POST.get('prenom')
        nom = request.POST.get('nom')
        nom_parc = request.POST.get('nom')
        adressparc = request.POST.get('adressparc')
        location = geocoder.osm(adressparc)
        lat = location.lat
        long = location.lng
        user = User.objects.create_user(
            username=username, email=email, password=passing, first_name=prenom, last_name=nom)
        user.save()
        InfoParc = Parc.objects.create(user=user,
                                         nom_parc=nom_parc, adresse=adressparc,)
        InfoParc.save()
        ajout = Parc.objects.get(pk=InfoParc.id)
        ajout.alt = location.lat
        ajout.long = location.lng
        ajout.save()
    return render(request, 'pages/ajoute.html')

@staff_member_required
def administrator1(request):
    list_parc = Parc.objects.all()
    err = (((Parc.objects.all()).exclude(nbr_err=0)).exclude(demande_s=True))
    normal = Parc.objects.filter(nbr_err=0, demande_s=False)
    delete = Parc.objects.filter(demande_s=True)
    m = folium.Map(location=[31.792305849269, -7.080168000000015],
                   width=820, height=492, zoom_start=7)
    for erreur in err:
        folium.Marker([erreur.alt, erreur.long], tooltip='parc have a Errors',
                      popup=erreur.adresse, icon=folium.Icon(color='orange')).add_to(m)
    for norm in normal:
        folium.Marker([norm.alt, norm.long], tooltip='Parc Etat Normale',
                      popup=norm.adresse, icon=folium.Icon(color='green')).add_to(m)
    for liste in delete:
        folium.Marker([liste.alt, liste.long], tooltip='Demande of Delete',
                      popup=liste.adresse, icon=folium.Icon(color='red')).add_to(m)

    m = m._repr_html_()

    context = {'list_parc': list_parc,
               'list_err': err,
               'list_normal': normal,
               'list_delete': delete,
               'count_err': (((Parc.objects.all()).exclude(nbr_err=0)).exclude(demande_s=True)).count(),
               'count_normale': Parc.objects.filter(nbr_err=0, demande_s=False).count(),
               'count_delete': Parc.objects.filter(demande_s=True).count(),
               'count_all': Parc.objects.all().count(),

               'map': m, }

    return render(request, 'pages/administrator.html', context)


def login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    users = authenticate(username=username, password=password)
    if request.method == "POST":
        if users.is_active:
            if users.is_staff:
                return redirect('/administrator')

    return render(request, 'pages/login.html')


def logout1(request):
    logout(request)
    return redirect('/administrator/login')

@staff_member_required
def suppression_parc(request):
    context = {'list_sup':  Parc.objects.filter(demande_s=True)}
    return render(request, 'pages/page_delete.html', context)

@staff_member_required
def deleteParc(request, id):
    pr = Parc.objects.get(pk=id)
    if User.objects.filter(username=pr.user).exists():
        pr.delete()
        User.objects.filter(username=pr.user).delete()
    return redirect('/administrator/demadesuppression')

@staff_member_required
def errorPage(request):
    context = {'list_errors': Parc.objects.exclude(nbr_err=0)}
    return render(request, 'pages/errors_page.html', context)

@staff_member_required
def deleteError(request, id):
    error = Parc.objects.get(pk=id)
    machine_erreur = Machine.objects.filter(parc=id)
    error.nbr_err = 0
    error.nbr_ram = 0
    error.nbr_dd = 0
    error.nbr_os = 0
    error.nbr_af = 0
    error.save()
    for liste in machine_erreur:
        liste.probleme_ram = ""
        liste.probleme_os = ""
        liste.probleme_dd = ""
        liste.probleme_alimentation_affichage = ""
        liste.autre_probleme = ""
        liste.save()
    return redirect('/administrator/errors')

@staff_member_required
def render_pdf_ones(request, id):
    obj_err = get_object_or_404(Parc, pk=id)
    template_path = 'Render_pdf/pdf_ones.html'
    context = {'One': obj_err,
               'machine': Machine.objects.filter(parc=id), }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

@staff_member_required
def render_pdf_all(request):
    template_path = 'Render_pdf/pdf_all.html'
    context = {
        'All': (((Parc.objects.all()).exclude(nbr_err=0)).exclude(demande_s=True)),
        'machine': Machine.objects.all(), }
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'filename="report.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response

