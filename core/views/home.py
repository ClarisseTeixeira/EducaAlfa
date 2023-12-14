from datetime import date, timedelta, datetime
from django.db.models import Count
from django.shortcuts import render
from revisao.models import Revisao, Flashcard
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import user_passes_test
from core.views.auth import superuser
from materiais.models import *
from django.contrib.auth.models import User
from django.contrib import messages
from core.models import Profile
from questoes.views import grafico, estatisticas
from questoes.models import UserProfile

 
def index(request):
    return render(request, "index.html")

def home(request):
    return render(request, "core/home.html")

@login_required
def dashboard(request):
    user = request.user
    created = Profile.objects.get_or_create(user=user)
    todas_revisoes = Revisao.objects.filter(user=user, concluida=False, data_agendada__gte=date.today()).order_by('data_agendada')
    revisoes_do_dia = Revisao.objects.filter(user=user, data_agendada=date.today(), concluida=False)
    revisoes_pendentes = Revisao.objects.filter(user=user, data_agendada__lt=date.today(), concluida=False)
    revisao = Revisao.objects.filter(user=user, concluida=False, data_agendada__lte=date.today()).order_by('data_agendada').first()

    if request.user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    acertos = user_profile.acertos
    erros = user_profile.erros

    if acertos + erros > 0:
        taxa_acerto = round((acertos / (acertos + erros)) * 100, 2)
    else:
       taxa_acerto = 0

    serialized_data = revisoes(user) 
    serialized_dataq = grafico(request)

    context = {
        'todas_revisoes': todas_revisoes,
        'revisoes_do_dia': revisoes_do_dia,
        'revisoes_pendentes': revisoes_pendentes,
        'serialized_data': serialized_data,
        'revisao': revisao,
        'serialized_dataq': serialized_dataq,
        'taxa_acerto': taxa_acerto,
    }

    return render(request, "core/pages/dashboard.html", context)


def revisoes(user):
    today = datetime.now().date()
    inicio = today - timedelta(days=today.weekday()) + timedelta(days=1)
    fim = inicio + timedelta(days=6)
    
    data = (
        Revisao.objects
        .filter(user=user, concluida=True, data_agendada__range=[inicio, fim])
        .values('data_agendada')
        .annotate(revisoes=Count('id'))
        .order_by('data_agendada')
    )

    weekdays = ['Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb']
    revisoes_por_dia = [0] * len(weekdays)

    for item in data:
        data_agendada = item['data_agendada'] + timedelta(days=1)
        dia_da_semana = data_agendada.weekday()
        revisoes_por_dia[dia_da_semana] = item['revisoes']
 
    data_to_serialize = {
        'weekdays': weekdays,  
        'revisoes': revisoes_por_dia
        }
    return json.dumps(data_to_serialize)
 

@user_passes_test(superuser)
def arearestrita(request):
    disciplinas = Disciplina.objects.all()
    assuntos = Assunto.objects.all()
    conteudos = Conteudo.objects.all()
    materiais = Materiais.objects.all()

    context = {
        'disciplinas': disciplinas,
        'assuntos': assuntos,
        'conteudos': conteudos,
        'materiais': materiais,
    }

    return render(request, 'core/pages/arearestrita.html', context)
