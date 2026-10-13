from django.core.paginator import Paginator
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response

from .models import Prestamo
from .serializers import PrestamoSerializer

#-----------------------------------------------------------------------------------------------

def paginar_prestamos(queryset, page_number):
    paginator = Paginator(queryset, 5)
    page = paginator.get_page(page_number)
    return Response({
        'pagina_actual': page.number,
        'total_paginas': paginator.num_pages,
        'total_registros': paginator.count,
        'resultados': PrestamoSerializer(page.object_list, many=True).data
    })

#-----------------------------------------------------------------------------------------------

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def prestamos_api(request):
    if request.method == 'GET':
        prestamos = Prestamo.objects.select_related('equipo').order_by('-fecha_prestamo')
        estado = request.query_params.get('estado')
        equipo = request.query_params.get('equipo')

        if estado:
            prestamos = prestamos.filter(estado=estado.upper())
        if equipo:
            if not equipo.isdigit():
                return Response({'equipo': 'Debe indicar el id del equipo...'}, status=400)
            prestamos = prestamos.filter(equipo_id=equipo)

        return paginar_prestamos(prestamos, request.query_params.get('page', 1))

    es_prestamista = request.user.groups.filter(name='Prestamistas').exists()
    if not es_prestamista or not request.user.has_perm('prestamos.add_prestamo'):
        return Response({'detail': 'Debe pertenecer al grupo Prestamistas para crear préstamos...'}, status=403)

    serializer = PrestamoSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#-----------------------------------------------------------------------------------------------

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def prestamo_detalle_api(request, id):
    try:
        prestamo = Prestamo.objects.select_related('equipo').get(id=id)
    except Prestamo.DoesNotExist:
        return Response({'error': 'Préstamo no encontrado...'}, status=404)

    if request.method == 'GET':
        return Response(PrestamoSerializer(prestamo).data)

    if request.method in ['PUT', 'PATCH']:
        if not request.user.has_perm('prestamos.change_prestamo'):
            return Response({'detail': 'No tiene permiso para modificar préstamos...'}, status=403)

        serializer = PrestamoSerializer(
            prestamo, data=request.data,
            partial=request.method == 'PATCH'
        )
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    if not IsAdminUser().has_permission(request, None):
        return Response({'detail': 'Solo un administrador puede eliminar préstamos...'}, status=403)

    prestamo.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)

#-----------------------------------------------------------------------------------------------
