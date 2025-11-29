from django.contrib.auth.models import User
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('id','first_name','last_name', 'email')

class AdminSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Administradores
        fields = '__all__'
        
class AlumnoSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Alumnos
        fields = "__all__"

class MaestroSerializer(serializers.ModelSerializer):
    user=UserSerializer(read_only=True)
    class Meta:
        model = Maestros
        fields = '__all__'

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventos
        fields = '__all__'

    from rest_framework import serializers
from .models import Eventos

class EventoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eventos
        fields = '__all__'

    def validate(self, data):

        hora_inicio = data.get('hora_inicio')
        hora_fin = data.get('hora_fin')

        if self.instance:
            if not hora_inicio:
                hora_inicio = self.instance.hora_inicio
            if not hora_fin:
                hora_fin = self.instance.hora_fin

        if hora_inicio and hora_fin:

            if hora_inicio >= hora_fin:
                raise serializers.ValidationError({
                    "hora_fin": "La hora de finalización debe ser posterior a la hora de inicio."
                })

        return data