from django.contrib import admin
from .models import Agente, Casuistica

admin.site.register(Agente)
admin.site.register(Casuistica)
class CasuisticaAdmin(admin.ModelAdmin):
    filter_horizontal = ('agentes_asignados',) #Esto permite ver los agentes en un panel horizontal

