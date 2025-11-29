from .models import Administradores, Maestros, Alumnos

def es_admin(user):
    return Administradores.objects.filter(user=user).exists()

def es_maestro(user):
    return Maestros.objects.filter(user=user).exists()

def es_alumno(user):
    return Alumnos.objects.filter(user=user).exists()