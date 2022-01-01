from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import HomeView, MachineDetailView, MachineCreateView, MachineUpdateView, MachineView, MachineDeleteView, RedirectView, mapview, suppresion
urlpatterns = [
    path('home/', HomeView, name='home'),
    path('map/', mapview, name='mapv'),
    path('add_machine/', login_required(MachineCreateView.as_view(), login_url="/login/"), name="machine-add"),
    path('machine/<int:pk>', login_required(MachineDetailView.as_view(), login_url="/login/"), name="machine-detail"),
    path('machine/<int:pk>/edit', login_required(MachineUpdateView.as_view(), login_url="/login/"), name="machine-update"),
    path('machine/<int:pk>/delete', login_required(MachineDeleteView.as_view(), login_url="/login/"), name="machine-delete"),
    path('machine/views', login_required(MachineView.as_view(), login_url="/login/"), name="machine-view"),
    path('', RedirectView, name="redirect-home"),
    path('parc/delete', suppresion, name="delete-parc"),
]