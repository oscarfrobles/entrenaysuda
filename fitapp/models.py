from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
# Create your models here.



class Tipo(models.TextChoices):
    ANAEROBICO = 1, 'Anaeróbico'
    AEROBICO = 2, 'Aeróbico'

class Zona(models.TextChoices):
    SUPERIOR = 1, 'Superior'
    INFERIOR = 2, 'Tren inferior'
    FULL = 3, 'Full body'

class Nivel(models.TextChoices):
    INICIAL = 1, 'Inicial'
    MEDIO = 2, 'Medio'
    AVANZADO = 3, 'Avanzado'

class Series(models.IntegerChoices):
    UNO = 1, '1'
    DOS = 2, '2'
    TRES = 3, '3'
    CUATRO = 4, '4'
    CINCO = 5, '5'
    SEIS = 6, '6'
    SIETE = 7, '7'
    OCHO = 8, '8'
    NUEVE = 9, '9'
    DIEZ = 10, '10'


class Ejercicio(models.Model):
    nombre = models.CharField(max_length=120)
    tipo = models.CharField(
        max_length=1,
        choices=Tipo.choices,
        default=Tipo.ANAEROBICO,
    )
    zona = models.CharField(
        max_length=1,
        choices=Zona.choices,
        default=Zona.INFERIOR,
    )
    reps = models.CharField(max_length=20, default='', blank=True)
    tiempo = models.CharField(max_length=20, help_text="Tiempo en segundos", default='', blank=True)
    imagen = models.ImageField(upload_to='img/', verbose_name="Imagen", blank=True, default='')
    url = models.CharField(default='',max_length=120, help_text="Url de vídeo", verbose_name="Vídeo", blank=True)
    nivel = models.CharField(
        max_length=1,
        choices=Nivel.choices,
        default=Nivel.INICIAL,
    )
    instagram_code =  models.TextField(default='', help_text="Código Instagram", verbose_name="Instagram code insertion", blank=True)
    indicaciones = models.CharField(max_length=255, default='', blank=True)
    orden = models.IntegerField(default=10)
    def __str__(self):
        return self.nombre
    class Meta:
        ordering = ['orden']

class Medida(models.Model):
    MONTH_CHOICES = ((1, "Enero"), (2, "Febrero"), (3, "Marzo"),(4, "Abril"),(5, "Mayo"),(6, "Junio"),(7, "Julio"),(8, "Agosto"),(9, "Septiembre"),(10, "Octubre"),(11, "Noviembre"),(12, "Diciembre"),)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    date = date.today()
    year = date.strftime("%Y")
    month = date.month
    anyo = models.IntegerField(default=year, verbose_name="Año")
    mes = models.IntegerField(choices=MONTH_CHOICES, verbose_name="Mes", default=month)
    peso = models.FloatField(blank=False,  default=float('30.0'))
    imc = models.FloatField(blank=True,  default=float('0.0'))
    grasa = models.FloatField(blank=True,  default=float('0.0'))
    musculo = models.FloatField(blank=True,  default=float('0.0'))
    cintura = models.FloatField(blank=True,  default=float('0.0'))
    pecho = models.FloatField(blank=True,  default=float('0.0'))
    biceps = models.FloatField(blank=True,  default=float('0.0'))
    muslo = models.FloatField(blank=True,  default=float('0.0'))
    gemelo = models.FloatField(blank=True,  default=float('0.0'))
    caliper = models.FloatField(blank=True,  default=float('0.0'))

    class Meta:
        unique_together = (('mes', 'anyo', 'user'),)

class EntrenamientoCompletado(models.IntegerChoices):
    INCOMPLETO = 0, ('NO REALIZADO')
    COMPLETO = 1, ('COMPLETO')
    SEMICOMPLETO = 2, ('SEMICOMPLETO')

class SesionesGoogle(models.Model):
    id_google = models.CharField(unique=True, max_length=200)
    name    = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200, blank=True)
    start = models.BigIntegerField()
    end = models.BigIntegerField()
    duration = models.FloatField(blank=True,  default=float('0.0'))
    activityType = models.IntegerField()
    application = models.CharField(max_length=200, blank=True)
    user_google = models.CharField(max_length=200, blank=True)


    def __str__(self):
        str = ''
        if self.name.__sizeof__() > 0:
            str += self.name
        if self.description.__sizeof__() > 0:
            str += self.description
        if len(str) == 0:
            str = self.id_google
        return str


class Calendario(models.Model):
    fecha = models.DateField(("Fecha"), default=date.today)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default='1')
    ejercicios = models.ManyToManyField(Ejercicio, related_name="ejercicios")
    series = models.IntegerField(
                 choices=Series.choices,
                 default=Series.UNO,
    )
    comentario = models.CharField(max_length=300, default='', blank=True)
    completado = models.IntegerField(default=EntrenamientoCompletado.INCOMPLETO, choices=EntrenamientoCompletado.choices)
    activo = models.BooleanField(default=True)
    calories = models.IntegerField(blank=True, null=True)
    steps = models.IntegerField(blank=True, null=True)
    estimated_steps = models.IntegerField(blank=True, null=True)
    distance = models.IntegerField(blank=True, null=True)
    heart = models.IntegerField(blank=True, null=True)
    bpm = models.IntegerField(blank=True, null=True)
    weight = models.FloatField(blank=True, null=True)
    #session_google = ArrayField(models.ForeignKey(SesionesGoogle, on_delete=models.DO_NOTHING, null=True, blank=True))
    session_google = models.ManyToManyField(SesionesGoogle,blank=True, null=True )


    def __str__(self):
        return str(self.fecha) + ' ' + str(self.user).upper()
    class Meta:
        ordering = ['fecha']

