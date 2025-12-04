from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authentication import TokenAuthentication
from django.contrib.auth.models import AbstractUser, User
from django.conf import settings

from django.db import models
from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication

from django.core.validators import MinValueValidator, MaxValueValidator
from .validatos import validar_fecha_no_pasada, validador_alfanumerico, validador_puntuacion
from django.core.exceptions import ValidationError

class BearerTokenAuthentication(TokenAuthentication):
    keyword = "Bearer"

class Administradores(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    clave_admin = models.CharField(max_length=255,null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    ocupacion = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del admin "+self.user.first_name+" "+self.user.last_name

class Alumnos(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    matricula = models.CharField(max_length=255,null=True, blank=True)
    curp = models.CharField(max_length=255,null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    ocupacion = models.CharField(max_length=255,null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del alumno "+self.user.first_name+" "+self.user.last_name
    
class Maestros(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, default=None)
    id_trabajador = models.CharField(max_length=255,null=True, blank=True)
    fecha_nacimiento = models.DateTimeField(auto_now_add=False, null=True, blank=True)
    telefono = models.CharField(max_length=255, null=True, blank=True)
    rfc = models.CharField(max_length=255,null=True, blank=True)
    cubiculo = models.CharField(max_length=255,null=True, blank=True)
    edad = models.IntegerField(null=True, blank=True)
    area_investigacion = models.CharField(max_length=255,null=True, blank=True)
    materias_json = models.TextField(null=True, blank=True)
    creation = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "Perfil del maestro "+self.user.first_name+" "+self.user.last_name 

class Eventos(models.Model):

    class TIPOS_EVENTOS(models.TextChoices):
        CONFERENCIA = 'conferencia', 'Conferencia'
        TALLER = 'taller', 'Taller'
        SEMINARIO = 'seminario', 'Seminario'
        CONCURSO = 'concurso', 'Concurso'
    
    class PUBLICO_OBJETIVO(models.TextChoices):
        ALUMNOS = 'alumnos', 'Alumnos'
        MAESTROS = 'maestros', 'Maestros'
        PUBLICO_GENERAL = 'publico_general', 'Público General'

    class PROGRAMAS_EDUCATIVOS(models.TextChoices):
        INGENIERIA_CIENCIAS_COMPUTACION = 'ingenieria_ciencias_computacion', 'Ingeniería en Ciencias de la Computación'
        LICENCIATURA_CIENCIAS_COMPUTACION = 'licenciatura_ciencias_computacion', 'Licenciatura en Ciencias de la Computación'
        INGENIERIA_TECNOLOGIAS_INFORMACION = 'ingenieria_tecnologias_informacion', 'Ingeniería en Tecnologías de la Información'

    nombre = models.CharField(max_length=255, null=False, blank=False, validators=[validador_alfanumerico])
    tipo = models.CharField(max_length=50, choices=TIPOS_EVENTOS.choices, null=False, blank=False)
    fecha = models.DateField(null=False, blank=False, validators=[validar_fecha_no_pasada])
    hora_inicio = models.TimeField(null=False, blank=False)
    hora_fin = models.TimeField(null=False, blank=False)
    lugar = models.CharField(max_length=255, null=False, blank=False, validators=[validador_alfanumerico])
    publico_objetivo = models.CharField(max_length=50, choices=PUBLICO_OBJETIVO.choices, null=False, blank=False)
    programa_educativo = models.CharField(max_length=50, choices=PROGRAMAS_EDUCATIVOS.choices, null=True, blank=True)
    responsable = models.CharField(max_length=255, null=False, blank=False)
    descripcion =models.TextField(max_length=300, null=False, blank=False, validators=[validador_puntuacion])
    cupo_max = models.IntegerField(null=False, blank=False, validators=[MinValueValidator(1), MaxValueValidator(999)])

