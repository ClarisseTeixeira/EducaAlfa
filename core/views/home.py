from datetime import date, timedelta, datetime
from django.db.models import Count
from django.shortcuts import render
from revisao.models import Revisao  
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json

def index(request):
    return render(request, "index.html")


def home(request):
    return render(request, "core/home.html")

@login_required
def dashboard(request):
    user = request.user

    todas_revisoes = Revisao.objects.filter(user=user, data_agendada__gte=date.today()).order_by('data_agendada')

    revisoes_do_dia = Revisao.objects.filter(user=user, data_agendada=date.today(), concluida=False)

    revisoes_pendentes = Revisao.objects.filter(user=user, data_agendada__lt=date.today(), concluida=False)

    # Recupere dados para o gráfico
    start_of_week, end_of_week = semana_atual()
    data = Revisao.objects.filter(
        concluida=True,
        data_agendada__range=[start_of_week, end_of_week]
    ).values('data_agendada').annotate(
        revisoes=Count('id')
    ).order_by('data_agendada').filter(user=request.user)

    # Crie uma lista de valores (quantidade de revisões) para cada dia da semana
    weekdays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
    revisoes_por_dia = [0] * len(weekdays)

    # Recupere as revisões concluídas e agrupe-as por dia da semana
    for item in data:
        data_agendada = item['data_agendada']
        day_of_week = data_agendada.weekday()
        revisoes_por_dia[day_of_week] = item['revisoes']

    # Serializa os dados em JSON
    data_to_serialize = {
        'weekdays': weekdays,
        'revisoes': revisoes_por_dia,
    }

    serialized_data = json.dumps(data_to_serialize)

    context = {
        'todas_revisoes': todas_revisoes,
        'revisoes_do_dia': revisoes_do_dia,
        'revisoes_pendentes': revisoes_pendentes,
        'serialized_data': serialized_data,  # Adicione os dados serializados ao contexto
    }
    return render(request, "core/pages/dashboard.html", context)




def semana_atual():
    today = datetime.now()
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(days=1)
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week

def revisoes(request):
    start_of_week, end_of_week = semana_atual()
    
    data = Revisao.objects.filter(
        concluida=True,
        data_agendada__range=[start_of_week, end_of_week]
    ).values('data_agendada').annotate(
        revisoes=Count('id')
    ).order_by('data_agendada')
    
    # Crie uma lista de valores (quantidade de revisões) para cada dia da semana
    weekdays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb' ]
    revisoes_por_dia = [0] * len(weekdays)
    
    # Recupere as revisões concluídas e agrupe-as por dia da semana
    for item in data:
        data_agendada = item['data_agendada']
        day_of_week = data_agendada.weekday()
        revisoes_por_dia[day_of_week] = item['revisoes']
    
    # Serializa os dados em JSON
    data_to_serialize = {
        'weekdays': weekdays,
        'revisoes': revisoes_por_dia,
    }
    
    serialized_data = json.dumps(data_to_serialize)
    
    context = {'weekdays': weekdays, 
               'revisoes': revisoes_por_dia,
               'serialized_data': serialized_data}  # Adicione os dados serializados ao contexto
    
    return render(request, 'revisao/grafico.html', context)