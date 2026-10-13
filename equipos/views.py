import json

from django.core.paginator import Paginator
from django.db.models import ProtectedError
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Equipo
from .serializers import EquipoSerializer

#-----------------------------------------------------------------------------------------------

def paginar_equipos(queryset, page_number):
    paginator = Paginator(queryset, 5)
    page = paginator.get_page(page_number)
    return Response({
        'pagina_actual': page.number,
        'total_paginas': paginator.num_pages,
        'total_registros': paginator.count,
        'resultados': EquipoSerializer(page.object_list, many=True).data
    })

#-----------------------------------------------------------------------------------------------

@api_view(['GET', 'POST'])
def equipos_api(request):
    if request.method == 'GET':
        equipos = Equipo.objects.all()
        categoria = request.query_params.get('categoria')
        ordering = request.query_params.get('ordering', 'nombre')

        if categoria:
            equipos = equipos.filter(categoria__iexact=categoria)

        if ordering not in ['nombre', '-nombre']:
            ordering = 'nombre'
        equipos = equipos.order_by(ordering)

        return paginar_equipos(equipos, request.query_params.get('page', 1))

    if not request.user.is_authenticated:
        return Response({'detail': 'Debe enviar el token de autenticación...'}, status=401)
    if not request.user.has_perm('equipos.add_equipo'):
        return Response({'detail': 'No tiene permiso para crear equipos...'}, status=403)

    serializer = EquipoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-----------------------------------------------------------------------------------------------

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def equipo_detalle_api(request, id):
    try:
        equipo = Equipo.objects.get(id=id)
    except Equipo.DoesNotExist:
        return Response({'error': 'Equipo no encontrado...'}, status=404)

    if request.method == 'GET':
        return Response(EquipoSerializer(equipo).data)

    if not request.user.is_authenticated:
        return Response({'detail': 'Debe enviar el token de autenticación...'}, status=401)

    if request.method in ['PUT', 'PATCH']:
        if not request.user.has_perm('equipos.change_equipo'):
            return Response({'detail': 'No tiene permiso para modificar equipos...'}, status=403)

        serializer = EquipoSerializer(
            equipo, data=request.data,
            partial=request.method == 'PATCH'
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if not request.user.has_perm('equipos.delete_equipo'):
        return Response({'detail': 'No tiene permiso para eliminar equipos...'}, status=403)

    try:
        equipo.delete()
    except ProtectedError:
        return Response({'error': 'No se puede eliminar un equipo que tiene préstamos registrados...'}, status=400)
    return Response(status=status.HTTP_204_NO_CONTENT)

#-----------------------------------------------------------------------------------------------

def preferencia_sesion(request):
    if request.method == 'GET':
        return JsonResponse({
            'categoria_preferida': request.session.get('categoria_preferida'),
            'csrftoken': get_token(request)
        })

    if request.method == 'POST':
        try:
            datos = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Debe enviar un JSON válido...'}, status=400)

        categoria = str(datos.get('categoria_preferida', '')).strip()

        if not categoria:
            return JsonResponse({'categoria_preferida': 'Este campo es obligatorio...'}, status=400)
        if len(categoria) > 50:
            return JsonResponse({'categoria_preferida': 'Máximo 50 caracteres...'}, status=400)

        request.session['categoria_preferida'] = categoria
        return JsonResponse({
            'mensaje': 'Preferencia guardada en la sesión...',
            'categoria_preferida': categoria
        })

    return JsonResponse({'error': 'Método no permitido...'}, status=405)

#-----------------------------------------------------------------------------------------------
