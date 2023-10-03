from django.shortcuts import render, get_object_or_404, redirect
from .models import Disciplina, Assunto, Questao, Alternativa
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User  # Importe User corretamente
import json
from django.http import JsonResponse


@login_required
def grafico(request, usuario_id):
    user = User.objects.get(id=usuario_id)
    questoes_certas = user.questoes.filter(correta=True).count()
    questoes_erradas = user.questoes.filter(correta=False).count()
    
    data = {
        'questoes_certas': questoes_certas,
        'questoes_erradas': questoes_erradas,
    }
    
    # Converta os dados em JSON
    data_json = json.dumps(data)
    
    return render(request, 'questoes/partials/grafico.html', {'data_json': data_json})


@login_required
def lista_questoes(request):
    disciplinas = Disciplina.objects.all()
    questoes = Questao.objects.all()
    context = {
        'disciplinas': disciplinas, 
        'questoes': questoes,
    }
    return render(request, 'questoes/pages/lista_questoes.html', context)


def filtro_questoes(request):
    disciplinas = Disciplina.objects.all()

    # Obtém a disciplina selecionada a partir do parâmetro 'disciplina' na requisição GET
    disciplina_id = request.GET.get('disciplina')

    # Filtra os assuntos com base na disciplina selecionada
    assuntos = []
    if disciplina_id:
        assuntos = Assunto.objects.filter(disciplina_id=disciplina_id)

    # Obtém a questão selecionada a partir do parâmetro 'assunto' na requisição GET
    assunto_id = request.GET.get('assunto')

    # Filtra as questões com base na disciplina e assunto selecionados
    questoes = Questao.objects.all()
    if disciplina_id:
        questoes = questoes.filter(disciplina_id=disciplina_id)
    if assunto_id:
        questoes = questoes.filter(assunto_id=assunto_id)

    # Define o número de questões por página
    questoes_por_pagina = 5
    paginator = Paginator(questoes, questoes_por_pagina)

    # Obtém o número da página a partir da consulta GET
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    return render(request, 'questoes/pages/lista_questoes.html', {
        'disciplinas': disciplinas,
        'assuntos': assuntos,
        'questoes': page,
        'disciplina_selecionada': int(disciplina_id) if disciplina_id else None,  # Converte para int se não for None
        'assunto_selecionado': int(assunto_id) if assunto_id else None,  # Converte para int se não for None
    })

@login_required
def verificar_resposta(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)

    if request.method == 'POST':
        alternativa_id = request.POST.get('alternativa')
        alternativa_selecionada = get_object_or_404(Alternativa, pk=alternativa_id)

        if alternativa_selecionada.correta:
            mensagem = 'acertou!'
            questao.acertou = True
        else:
            mensagem = 'errou.'

        # Marque a questão como respondida
        questao.respondida = True
        questao.save()

        questoes_certas = Questao.objects.filter(respondida=True, acertou=True).count()
        questoes_erradas = Questao.objects.filter(respondida=True, acertou=False).count()
        questoes_respondidas = Questao.objects.filter(respondida=True).count()

        # Adicione as informações ao dicionário 'data'
        data = {
            'questoes_certas': questoes_certas,
            'questoes_erradas': questoes_erradas,
            'questoes_respondidas': questoes_respondidas,
        }

        # Retorne os dados atualizados como uma resposta JSON
        return JsonResponse(data)

    return redirect('questoes', questao_id=questao_id)
