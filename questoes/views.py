from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Disciplina, Assunto, Questao, Alternativa, UserProfile
from django.contrib.auth.models import User
import json
from django.contrib import messages
from .forms import QuestaoForm
from django.contrib.auth.decorators import user_passes_test
from core.views.auth import superuser
from django.db.models import Sum, Count, Q, Case, When, F, IntegerField
from .models import Disciplina, UserProfile, Questao, Resposta

@login_required
def estatisticas(request):
    # Obtém as disciplinas disponíveis
    disciplinas = Disciplina.objects.all()

    # Inicializa uma lista para armazenar os dados de cada disciplina
    dados_disciplinas = []

    # Se o usuário estiver autenticado, obtenha os dados reais do usuário
    if request.user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Adiciona os dados do usuário à lista
        dados_usuario = {
            'questoes_certas': user_profile.questoes_certas or 0,
            'questoes_erradas': user_profile.questoes_erradas or 0,
            'taxa_acerto': user_profile.taxa_acerto(),
            'num_questoes': user_profile.num_questoes(),
        }

        for disciplina in disciplinas:
            # Filtra as questões por disciplina
            questoes_disciplina = Questao.objects.filter(disciplina=disciplina)

            # Obtém o número total de respostas do usuário para cada disciplina
            num_questoes_disciplina = Resposta.objects.filter(
                alternativa__questao__in=questoes_disciplina,
                user_profile=user_profile
            ).count()

            # Obtém o número de respostas certas e erradas do usuário para cada disciplina
            questoes_certas = Resposta.objects.filter(
                alternativa__questao__in=questoes_disciplina,
                user_profile=user_profile,
                certa=True
            ).count()

            questoes_erradas = Resposta.objects.filter(
                alternativa__questao__in=questoes_disciplina,
                user_profile=user_profile,
                certa=False
            ).count()

            # Adiciona os dados da disciplina à lista
            dados_disciplina = {
                'disciplina': disciplina,
                'questoes_certas': questoes_certas,
                'questoes_erradas': questoes_erradas,
                'num_questoes_respondidas': num_questoes_disciplina,
                'taxa_acerto': round((questoes_certas / (questoes_certas + questoes_erradas)) * 100, 2) if (questoes_certas + questoes_erradas) > 0 else 0,
            }

            dados_disciplinas.append(dados_disciplina)

    # Envie os dados para o template
    data = {
        'dados_usuario': dados_usuario,
        'dados_disciplinas': dados_disciplinas,
    }

    return render(request, 'questoes/pages/estatisticas.html', data)

@login_required
def lista_questoes(request):
    disciplinas = Disciplina.objects.all()
    questoes = Questao.objects.all()


    # Adicione a lógica de paginação aqui
    questoes_por_pagina = 5
    paginator = Paginator(questoes, questoes_por_pagina)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)


    context = {
        'disciplinas': disciplinas,
        'questoes': page,
    }
    return render(request, 'questoes/pages/lista_questoes.html', context)


@login_required
def filtro_questoes(request):
    disciplinas = Disciplina.objects.all()


    disciplina_id = request.GET.get('disciplina')


    assuntos = []
    if disciplina_id:
        # Recupere apenas os assuntos relacionados à disciplina selecionada
        assuntos = Assunto.objects.filter(disciplina_id=disciplina_id)


    assunto_id = request.GET.get('assunto')


    questoes = Questao.objects.all()
    if disciplina_id:
        questoes = questoes.filter(disciplina_id=disciplina_id)
    if assunto_id:
        questoes = questoes.filter(assunto_id=assunto_id)


    questoes_por_pagina = 5
    paginator = Paginator(questoes, questoes_por_pagina)


    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)


    return render(request, 'questoes/pages/lista_questoes.html', {
        'disciplinas': disciplinas,
        'assuntos': assuntos,
        'questoes': page,
        'disciplina_selecionada': int(disciplina_id) if disciplina_id else None,
        'assunto_selecionado': int(assunto_id) if assunto_id else None,
    })


def obter_assuntos(request):
    disciplina_id = request.GET.get('disciplina_id')
    assuntos = Assunto.objects.filter(disciplina_id=disciplina_id).values('id', 'assunto')
    return JsonResponse(list(assuntos), safe=False)
# Restante do seu código...


@login_required
def verificar_resposta(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        alternativa_id = request.POST.get('alternativa')
        alternativa_selecionada = get_object_or_404(Alternativa, pk=alternativa_id)

        # Crie uma instância de Resposta associada à alternativa selecionada e ao perfil do usuário
        resposta = Resposta.objects.create(alternativa=alternativa_selecionada, user_profile=user_profile, certa=alternativa_selecionada.correta)

        # Atualize o número de questões certas e erradas no perfil do usuário
        if alternativa_selecionada.correta:
            mensagem = 'acertou!'
            user_profile.questoes_certas += 1
        else:
            mensagem = 'errou.'
            user_profile.questoes_erradas += 1

        questao.respondida = True
        questao.save()
        user_profile.save()

        # Informações sobre as alternativas para destaque no HTML
        alternativas_info = [{
            'id': alternativa.id,
            'is_correta': alternativa.correta,
            'is_selecionada': alternativa == alternativa_selecionada,
        } for alternativa in questao.alternativas.all()]

        # Retorne os dados atualizados e informações sobre as alternativas
        data = {
            'questoes_certas': user_profile.questoes_certas,
            'questoes_erradas': user_profile.questoes_erradas,
            'taxa_acerto': user_profile.taxa_acerto(),
            'num_questoes': user_profile.num_questoes(),
            'alternativas_info': alternativas_info,
        }

        # Se preferir, pode retornar a resposta como JSON
        return render(request, 'questoes/pages/lista_questoes.html')

    return redirect('questoes', questao_id=questao_id)


def indexquestoes(request):
    return render(request, 'questoes/pages/indexquestoes.html')


def grafico(request, usuario_id):
    user = User.objects.get(id=usuario_id)
    disciplinas = Disciplina.objects.all()


    dados_disciplinas = []
    for disciplina in disciplinas:
        questoes_certas = user.questoes.filter(disciplina=disciplina, correta=True).count()
        questoes_erradas = user.questoes.filter(disciplina=disciplina, correta=False).count()


        dados_disciplinas.append({
            'disciplina_nome': disciplina.nome,
            'questoes_certas': questoes_certas,
            'questoes_erradas': questoes_erradas,
        })


    return render(request, 'questoes/pages/estatisticas.html', {'dados_disciplinas': dados_disciplinas})





@user_passes_test(superuser)
def questao_criar(request):
    if request.method == 'POST':
        form = QuestaoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Questão criada com sucesso!')
            form = QuestaoForm()
    else:
        form = QuestaoForm()

    return render(request, "questoes/forms/formsquestoes.html", {'form': form})

def questao_remover(request, id):
    questao = get_object_or_404(Questao, id=id)
    questao.delete()
    messages.success(request, 'Questão excluído com sucesso!')
    return redirect('arearestrita')


def questao_editar(request, id):
    questao = get_object_or_404(Questao, id=id)
    if request.method == 'POST':
        form = QuestaoForm(request.POST, request.FILES, instance=questao)
        if form.is_valid():
            form.save()
            return redirect('arearestrita')
    else:
        form = QuestaoForm(instance=questao)
    return render(request, 'questoes/forms/formsquestoes.html', {'form': form})
