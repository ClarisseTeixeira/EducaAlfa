from django.shortcuts import render, get_object_or_404, redirect
from .models import Disciplina, Assunto, Questao, Alternativa
from django.core.paginator import Paginator



def lista_questoes(request):
    disciplinas = Disciplina.objects.all()
    questoes = Questao.objects.all()
    return render(request, 'questoes/pages/lista_questoes.html', {'disciplinas': disciplinas, 'questoes': questoes})


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


def verificar_resposta(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)

    if request.method == 'POST':
        alternativa_id = request.POST.get('alternativa')
        alternativa_selecionada = get_object_or_404(Alternativa, pk=alternativa_id)

        if alternativa_selecionada.correta:
            mensagem = 'acertou!'
        else:
            mensagem = 'errou.'

            # Marque a questão como respondida
        questao.respondida = True
        questao.save()

        return render(request, 'questoes/resposta.html', {'mensagem': mensagem})

    return redirect('questoes', questao_id=questao_id)

