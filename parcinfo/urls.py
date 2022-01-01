from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('administrator/login', views.login, name='login_admin'),
    path('administrator', views.administrator1, name='administrartor'),
    path('administrator/ajouter&parc', views.ajoutparc, name='ajoute'),
    path('administrator/logout', views.logout1, name='logout'),
    path('administrator/delete/<int:id>/', views.deleteParc, name='delete_parc'),
    path('administrator/demadesuppression', views.suppression_parc, name='demande_suppression'),
    path('administrator/errors/<int:id>/', views.deleteError, name='delete_error'),
    path('administrator/errors', views.errorPage, name='error_page'),
    path('administrator/pdf/<int:id>/', views.render_pdf_ones, name='pfd-views'),
    path('administrator/pdfAll', views.render_pdf_all, name='pfd-all-views'),

]
