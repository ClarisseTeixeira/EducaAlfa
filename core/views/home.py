from datetime import date, timedelta, datetime
from django.db.models import Count
from django.shortcuts import render
from revisao.models import Revisao, Flashcard
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404, redirect, render


def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, "core/home.html")

@login_required
def dashboard(request):
    user = request.user

    todas_revisoes = get_revisions(user, concluida=False, data_agendada__gte=date.today()).order_by('data_agendada')
    revisoes_do_dia = get_revisions(user, data_agendada=date.today(), concluida=False)
    revisoes_pendentes = get_revisions(user, data_agendada__lt=date.today(), concluida=False)

    revisao = Revisao.objects.filter(user=user, concluida=False, data_agendada__lte=date.today()).order_by('data_agendada').first()


    serialized_data = revisoes(user)

    context = {
        'todas_revisoes': todas_revisoes,
        'revisoes_do_dia': revisoes_do_dia,
        'revisoes_pendentes': revisoes_pendentes,
        'serialized_data': serialized_data,
        'revisao':revisao,
    }
    return render(request, "core/pages/dashboard.html", context)

def get_revisions(user, **kwargs):
    return Revisao.objects.filter(user=user, **kwargs)

def revisoes(user):
    start_of_week, end_of_week = semana_atual()
    data = get_revisions(user, concluida=True, data_agendada__range=[start_of_week, end_of_week]) \
        .values('data_agendada').annotate(revisoes=Count('id')).order_by('data_agendada')

    weekdays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
    revisoes_por_dia = [0] * len(weekdays)

    for item in data:
        data_agendada = item['data_agendada'] + timedelta(days=1)  # Adicionando um dia
        day_of_week = data_agendada.weekday()
        revisoes_por_dia[day_of_week] = item['revisoes']

    data_to_serialize = {'weekdays': weekdays, 'revisoes': revisoes_por_dia}
    return json.dumps(data_to_serialize)

def semana_atual():
    today = datetime.now().date()  # Pegar somente a data atual, sem considerar a hora
    start_of_week = today - timedelta(days=today.weekday()) + timedelta(days=1)  # Início da semana, um dia depois
    end_of_week = start_of_week + timedelta(days=6)  # Fim da semana
    return start_of_week, end_of_week



