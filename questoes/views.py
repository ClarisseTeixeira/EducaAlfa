from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Disciplina, Assunto, Questao, Alternativa, UserProfile
import json
from .models import Disciplina, UserProfile, Questao, Resposta


@login_required
def estatisticas(request):
    disciplinas = Disciplina.objects.all()
    dados_disciplinas = []

    if request.user.is_authenticated:
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)

        acertos = user_profile.acertos
        erros = user_profile.erros
        num_questoes = acertos + erros
        if num_questoes > 0:
            taxa_acerto = round((acertos / num_questoes) * 100, 2)
        else:
            taxa_acerto = 0

        dados_usuario = {
            'acertos': acertos,
            'erros': erros,
            'taxa_acerto': taxa_acerto,
            'num_questoes': num_questoes,
        }

        for disciplina in disciplinas:
            questoes_disciplina = Questao.objects.filter(disciplina=disciplina)
            
            num_questoes_disciplina = Resposta.objects.filter(
                questao__in=questoes_disciplina,
                user_profile=user_profile,
            ).count()

            acertos = Resposta.objects.filter(
                questao__in=questoes_disciplina,
                user_profile=user_profile,
                certa=True
            ).count()

            erros = Resposta.objects.filter(
                questao__in=questoes_disciplina,
                user_profile=user_profile,
                certa=False
            ).count()

            dados_disciplina = {
                'disciplina': disciplina,
                'acertos': acertos,
                'erros': erros,
                'num_questoes_respondidas': num_questoes_disciplina,
                'taxa_acerto': round((acertos / (acertos + erros)) * 100, 2) if (acertos + erros) > 0 else 0,
            }

            dados_disciplinas.append(dados_disciplina)

    serialized_dataq = grafico(request)

    context = {
        'dados_usuario': dados_usuario,
        'dados_disciplinas': dados_disciplinas,
        'serialized_dataq': serialized_dataq,
    }

    return render(request, 'questoes/pages/estatisticas.html', context)

@login_required
def lista_questoes(request):
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

def obter_assuntos(request):
    disciplina_id = request.GET.get('disciplina_id')
    assuntos = Assunto.objects.filter(disciplina_id=disciplina_id).values('id', 'assunto')
    return JsonResponse(list(assuntos), safe=False)

@login_required
def verificar_resposta(request):
    if request.method == 'POST':
        acertos = 0
        erros = 0
        user_profile, created = UserProfile.objects.get_or_create(user=request.user)


        for questao in Questao.objects.all():
            resposta_id = request.POST.get(f'questao_{questao.id}')
            if resposta_id:
                alternativa = Alternativa.objects.filter(
                    questao_id=questao.id,
                    id=resposta_id
                ).first()

                if alternativa and alternativa.correta:
                    acertos += 1
                    Resposta.objects.create(
                        questao=questao,
                        alternativa=alternativa,
                        user_profile=user_profile,
                        certa=True)
                else:
                    erros += 1
                    Resposta.objects.create(
                        questao=questao,
                        alternativa=alternativa,
                        user_profile=user_profile,
                        certa=False)
                                    

        user_profile.acertos += acertos
        user_profile.erros += erros
        user_profile.save()
        
    return redirect('lista_questoes')

def grafico(request):
    serialize = {'grafico': []}
    if request.user.is_authenticated:
        user = request.user
        data = UserProfile.objects.filter(user=user).first()

        if data:
            acertos = data.acertos
            erros = data.erros

            if acertos == 0 and erros == 0:
                serialize['grafico'] = [0, 0, 1] 
            else:
                serialize['grafico'] = [acertos, erros]

        return json.dumps(serialize)

def indexquestoes(request):
    return render(request, 'questoes/pages/indexquestoes.html')
