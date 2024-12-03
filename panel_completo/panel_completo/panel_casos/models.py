from django.db import models

class Agente(models.Model):
    nombre = models.CharField(max_length=100)
    carga_trabajo = models.IntegerField(default=0) # Nuevo campo

    def __str__(self):
        return self.nombre


class Casuistica(models.Model):
    nombre = models.CharField(max_length=200)
    peso = models.IntegerField()
    agentes = models.ManyToManyField(Agente, blank=True, related_name='casuisticas')

    def __str__(self):
        return self.nombre