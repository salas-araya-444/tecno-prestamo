from django.urls import path
from . import views

urlpatterns = [
    path('', views.prestamos_api, name='prestamos_api'),

    path('<int:id>/', views.prestamo_detalle_api, name='prestamo_detalle_api'),
]
