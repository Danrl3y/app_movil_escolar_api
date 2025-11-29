from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone

def validar_fecha_no_pasada(fecha):
    hoy = timezone.now().date()
    if fecha < hoy:
        raise ValidationError("La fecha no puede ser anterior a hoy.")

validador_alfanumerico = RegexValidator(
    regex=r'^[a-zA-Z0-9 áéíóúüñÁÉÍÓÚÜÑ]+$', 
    message='Solo se permiten letras, números y espacios. No se permiten caracteres especiales.',
    code='alfanumerico_invalido'
)

validador_puntuacion = RegexValidator(
    regex=r'^[a-zA-Z0-9 áéíóúüñÁÉÍÓÚÜÑ.,\-_]+$', 
    message='Solo se permiten letras, números y signos de puntuación básicos.',
    code='puntuacion_invalida'
)