from django.shortcuts import render, get_object_or_404, redirect
from .models import Disciplina, Assunto, Questao, Alternativa
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

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

    disciplina_id = request.GET.get('disciplina')

    assuntos = []
    if disciplina_id:
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

def verificar_resposta(request, questao_id):
    questao = get_object_or_404(Questao, pk=questao_id)

    if request.method == 'POST':
        alternativa_id = request.POST.get('alternativa')
        alternativa_selecionada = get_object_or_404(Alternativa, pk=alternativa_id)

        if alternativa_selecionada.correta:
            mensagem = 'acertou!'
        else:
            mensagem = 'errou.'

        questao.respondida = True
        questao.save()

        return render(request, 'questoes/resposta.html', {'mensagem': mensagem})

    return redirect('questoes', questao_id=questao_id)

def estatisticas(request):
    return render(request, 'questoes/pages/estatisticas.html')

def indexquestoes(request):
    return render(request, 'questoes/pages/indexquestoes.html')

@login_required
def grafico(request, usuario_id):
    user = User.objects.get(id=usuario_id)
    questoes_certas = user.questoes.filter(correta=True).count()
    questoes_erradas = user.questoes.filter(correta=False).count()
   
    data = {
        'questoes_certas': questoes_certas,
        'questoes_erradas': questoes_erradas,
    }
   
    data_json = json.dumps(data)
   
    return render(request, 'questoes/partials/grafico.html', {'data_json': data_json})


