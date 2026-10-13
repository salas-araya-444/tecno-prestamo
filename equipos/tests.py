from rest_framework.test import APITestCase
from .models import Equipo

class EquiposTests(APITestCase):

    def setUp(self):
        Equipo.objects.create(codigo='LAP-001', nombre='Laptop Dell', categoria='Laptop')
        Equipo.objects.create(codigo='PRO-001', nombre='Proyector Epson', categoria='Proyector')

    def test_listar_equipos_es_publico_y_filtra(self):
        response = self.client.get('/api/equipos/?categoria=Laptop')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['total_registros'], 1)

    def test_crear_equipo_sin_token(self):
        response = self.client.post('/api/equipos/', {
            'codigo': 'TAB-001',
            'nombre': 'Tablet Samsung',
            'categoria': 'Tablet'
        }, format='json')
        self.assertEqual(response.status_code, 401)
