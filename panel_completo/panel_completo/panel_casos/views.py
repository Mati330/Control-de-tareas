from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseBadRequest
from .models import Agente, Casuistica
from .forms import AgenteCasuisticaForm # Importar el formulario combinado
from django.views.decorators.csrf import csrf_exempt
import json

def panel_vista(request):
    agentes = Agente.objects.all()
    casuisticas = Casuistica.objects.all()
    contexto = {'agentes': agentes, 'casuisticas': casuisticas}
    return render(request, 'panel_casos/panel.html', contexto)

def crear_agente_casuistica(request):
    if request.method == 'POST':
        form = AgenteCasuisticaForm(request.POST) #Usar el formulario combinado
        if form.is_valid():
            agente_seleccionado = form.cleaned_data['agente_form']
            Casuistica.objects.create(nombre=form.cleaned_data['nombre_casuistica'], peso=form.cleaned_data['peso_casuistica'], agente_asignado=agente_seleccionado)
            return redirect('panel_vista')
    else:
        form = AgenteCasuisticaForm() #Usar el formulario combinado
    return render(request, 'panel_casos/crear_agente_casuistica.html', {'form': form})

@csrf_exempt  # REMEMBER TO REMOVE THIS IN PRODUCTION! Use proper CSRF protection.
def asignar_casuistica(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            casuistica_id = data['casuistica_id']
            agente_ids = data['agente_ids']

            casuistica = Casuistica.objects.get(pk=casuistica_id)
            agentes = Agente.objects.filter(pk__in=agente_ids)

            for agente in agentes:
                agente.carga_trabajo += casuistica.peso  # Suma directamente al campo
                agente.save()                            # Guarda los cambios

            casuistica.agentes.add(*agentes) # Actualiza la relación ManyToMany

            agente_data = [{'id': a.id, 'nombre': a.nombre, 'carga_trabajo': a.carga_trabajo} for a in Agente.objects.all()]
            return JsonResponse({'success': True, 'agente_data': agente_data})
        except Casuistica.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Casuística no encontrada'})
        except Agente.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Agente no encontrado'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Error al decodificar JSON'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@csrf_exempt
def limpiar_asignaciones(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            casuistica_id = data['casuistica_id']

            casuistica = Casuistica.objects.get(pk=casuistica_id)
            casuistica.agentes.clear()  # Elimina todas las asignaciones de agentes a esta casuistica

            agente_data = [{'id': a.id, 'nombre': a.nombre, 'carga_trabajo': a.carga_trabajo()} for a in Agente.objects.all()]
            return JsonResponse({'success': True, 'agente_data': agente_data})

        except Casuistica.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Casuística no encontrada'})
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Error al decodificar JSON'})
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Error inesperado: {str(e)}'}) #Log this for production

    return JsonResponse({'success': False, 'error': 'Método no permitido'})

def panel_vista(request):
    agentes = Agente.objects.all()
    casuisticas = Casuistica.objects.all()
    contexto = {'agentes': agentes, 'casuisticas': casuisticas}
    return render(request, 'panel_casos/panel.html', contexto)