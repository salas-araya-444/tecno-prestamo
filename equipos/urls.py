from django.urls import path
from . import views

urlpatterns = [
    path('', views.equipos_api, name='equipos_api'),

    path('<int:id>/', views.equipo_detalle_api, name='equipo_detalle_api'),
]
