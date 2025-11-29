from rest_framework.views import APIView
from rest_framework.response import Response
from ..models import Eventos
from ..serializers import EventoSerializer

from django.db import transaction
from rest_framework import permissions
from django.shortcuts import get_object_or_404

from ..permisos import es_admin, es_maestro, es_alumno

class EventoOpcionesView(APIView):

    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        data = {
            "tipos_eventos": [
                {"value": key, "label": label} 
                for key, label in Eventos.TIPOS_EVENTOS.choices
            ],
            "publico_objetivo": [
                {"value": key, "label": label} 
                for key, label in Eventos.PUBLICO_OBJETIVO.choices
            ],
            "programas_educativos": [
                {"value": key, "label": label} 
                for key, label in Eventos.PROGRAMAS_EDUCATIVOS.choices
            ]
        }
        return Response(data)
    
class EventosAll(APIView):

    permission_classes = (permissions.IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        user = request.user

        if es_admin(user): 
            eventos = Eventos.objects.all().order_by("id")
            
        elif es_maestro(user): 
            eventos = Eventos.objects.filter(
                publico_objectivo__in=[
                    Eventos.PUBLICO_OBJETIVO.MAESTROS, 
                    Eventos.PUBLICO_OBJETIVO.PUBLICO_GENERAL
                ]
            ).order_by("id")
            
        elif es_alumno(user):
            eventos = Eventos.objects.filter(
                publico_objectivo__in=[
                    Eventos.PUBLICO_OBJETIVO.ALUMNOS, 
                    Eventos.PUBLICO_OBJETIVO.PUBLICO_GENERAL
                ]
            ).order_by("id")
            
        lista = EventoSerializer(eventos, many=True).data
        return Response(lista, 200)
    
class EventosView(APIView):
    
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        
        evento = get_object_or_404(Eventos, id = request.GET.get("id"))
        evento = EventoSerializer(evento, many=False).data
        
        return Response(evento, 200)
    
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        
        if not es_admin(request.user):
            return Response({"details": "No autorizado. Solo administradores."}, status=403)

        evento = EventoSerializer(data=request.data)
        
        if evento.is_valid():
            
            evento.save()
            return Response({"evento_created_id": evento.instance.id }, 201)

        return Response(evento.errors, status=400)
    
    @transaction.atomic
    def put(self, request, *args, **kwargs):

        if not es_admin(request.user):
            return Response({"details": "No autorizado. Solo administradores."}, status=403)

        evento = get_object_or_404(Eventos, id=request.data["id"])
        serializer = EventoSerializer(evento, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response({"details":"Evento actualizado"},200)
        return Response(serializer.errors, status=400)

    @transaction.atomic
    def delete(self, request, *args, **kwargs):

        if not es_admin(request.user):
            return Response({"details": "No autorizado. Solo administradores."}, status=403)

        evento = get_object_or_404(Eventos, id=request.GET.get("id"))
        try:
            evento.delete()
            return Response({"details":"Evento eliminado"},200)
        except Exception as e:
            return Response({"details":"Algo pasó al eliminar"},400)