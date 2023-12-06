from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Disciplina, Assunto, Questao, Alternativa, UserProfile
from django.contrib.auth.models import User
import json
from django.db.models import Count, Sum


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

            # Obtém o número total de questões para cada disciplina
            num_questoes_disciplina = questoes_disciplina.count()

            # Obtém o número de questões certas e erradas para cada disciplina
            dados_disciplina = questoes_disciplina.aggregate(
                questoes_certas=Sum('questoes_certas'),
                questoes_erradas=Sum('questoes_erradas'),
            )

            # Trata valores None como 0
            dados_disciplina['questoes_certas'] = dados_disciplina['questoes_certas'] or 0
            dados_disciplina['questoes_erradas'] = dados_disciplina['questoes_erradas'] or 0

            # Adiciona os dados da disciplina à lista
            dados_disciplina['disciplina'] = disciplina
            dados_disciplina['taxa_acerto'] = round((dados_disciplina['questoes_certas'] / (dados_disciplina['questoes_certas'] + dados_disciplina['questoes_erradas'])) * 100, 2) if (dados_disciplina['questoes_certas'] + dados_disciplina['questoes_erradas']) > 0 else 0
            dados_disciplina['num_questoes_respondidas'] = num_questoes_disciplina

            dados_disciplinas.append(dados_disciplina)

    # Adicione prints para debug
    print(dados_usuario)
    print(dados_disciplinas)

    # Envie os dados para o template
    data = {
        'dados_usuario': dados_usuario,
        'dados_disciplinas': dados_disciplinas,
    }

    return render(request, 'questoes/pages/estatisticas.html', data)

# No seu arquivo views.py


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


        if alternativa_selecionada.correta:
            mensagem = 'acertou!'
            user_profile.questoes_certas += 1
        else:
            mensagem = 'errou.'
            user_profile.questoes_erradas += 1


        questao.respondida = True
        questao.save()
        user_profile.save()


        # Retorne os dados atualizados para o gráfico
        data = {
            'questoes_certas': user_profile.questoes_certas,
            'questoes_erradas': user_profile.questoes_erradas,
            'taxa_acerto': user_profile.taxa_acerto(),  # Adicione esse método ao seu modelo UserProfile
            'num_questoes': user_profile.num_questoes(),
        }


        # Se preferir, pode retornar a resposta como JSON
        return JsonResponse(data)


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


    return render(request, 'questoes/partials/s.html', {'dados_disciplinas': dados_disciplinas})