from django.contrib.auth.models import Group, Permission, User
from rest_framework.test import APITestCase

from equipos.models import Equipo
from .models import Prestamo

class PrestamosTests(APITestCase):

    def setUp(self):
        self.equipo = Equipo.objects.create(codigo='LAP-001', nombre='Laptop Dell', categoria='Laptop')

        grupo = Group.objects.create(name='Prestamistas')
        grupo.permissions.add(
            Permission.objects.get(codename='add_prestamo'),
            Permission.objects.get(codename='change_prestamo')
        )
        self.usuario = User.objects.create_user(username='prestamista', password='Clave12345!')
        self.usuario.groups.add(grupo)
        self.client.force_authenticate(user=self.usuario)

    def test_fecha_devolucion_anterior(self):
        response = self.client.post('/api/prestamos/', {
            'equipo': self.equipo.id,
            'solicitante': 'Ana Mora',
            'fecha_prestamo': '2026-10-15',
            'fecha_devolucion': '2026-10-10'
        }, format='json')
        self.assertEqual(response.status_code, 400)

    def test_no_permite_dos_prestamos_activos(self):
        datos = {
            'equipo': self.equipo.id,
            'solicitante': 'Ana Mora',
            'fecha_prestamo': '2026-10-12',
            'fecha_devolucion': '2026-10-15'
        }
        response = self.client.post('/api/prestamos/', datos, format='json')
        self.assertEqual(response.status_code, 201)

        response = self.client.post('/api/prestamos/', datos, format='json')
        self.assertEqual(response.status_code, 400)

    def test_editar_el_mismo_prestamo(self):
        prestamo = Prestamo.objects.create(
            equipo=self.equipo, solicitante='Ana Mora',
            fecha_prestamo='2026-10-12', fecha_devolucion='2026-10-15'
        )
        response = self.client.patch(f'/api/prestamos/{prestamo.id}/', {
            'solicitante': 'Ana María Mora'
        }, format='json')
        self.assertEqual(response.status_code, 200)

    def test_eliminar_sin_ser_admin(self):
        prestamo = Prestamo.objects.create(
            equipo=self.equipo, solicitante='Ana Mora',
            fecha_prestamo='2026-10-12', fecha_devolucion='2026-10-15'
        )
        response = self.client.delete(f'/api/prestamos/{prestamo.id}/')
        self.assertEqual(response.status_code, 403)
