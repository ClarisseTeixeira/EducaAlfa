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
def processar_respostas(request):
    if request.method == 'POST':
        acertos = 0
        erros = 0
        for questao in Questao.objects.all():
            resposta_id = request.POST.get(f'questao_{questao.id}')
            if resposta_id:
                alternativa = Alternativa.objects.filter(
                    questao_id=questao.id,
                    id=resposta_id
                ).first()                
                if alternativa and alternativa.correta:
                    acertos += 1
                else:
                    erros += 1
        
        request.session['acertos'] = acertos
        request.session['erros'] = erros
        
        messages.success(request, 'Respostas processadas com sucesso!')
        return redirect('resultados')
    return redirect('formulario_questoes')




@login_required
def formulario_questoes(request):
    questoes = Questao.objects.all()
    return render(request, 'questoes/formulario_questoes.html', {'questoes': questoes})


@login_required
def resultados(request):
    acertos = request.session.get('acertos', 0)
    erros = request.session.get('erros', 0)

    contexto = {
        'acertos': acertos,
        'erros': erros
    }
    return render(request, 'questoes/resultados.html', contexto)

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
        print(dados_usuario)

        for disciplina in disciplinas:
            questoes_disciplina = Questao.objects.filter(disciplina=disciplina)
            
            # Get the number of responses for each discipline by the current user
            num_questoes_disciplina = Resposta.objects.filter(
                questao__in=questoes_disciplina,
                user_profile=user_profile,
            ).count()

            # Get the number of correct and incorrect responses for each discipline by the current user
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

            # Add discipline data to the list
            dados_disciplina = {
                'disciplina': disciplina,
                'acertos': acertos,
                'erros': erros,
                'num_questoes_respondidas': num_questoes_disciplina,
                'taxa_acerto': round((acertos / (acertos + erros)) * 100, 2) if (acertos + erros) > 0 else 0,
            }

            dados_disciplinas.append(dados_disciplina)


    # Send data to the template
    data = {
        'dados_usuario': dados_usuario,
        'dados_disciplinas': dados_disciplinas,
    }

    return render(request, 'questoes/pages/estatisticas.html', data)

@login_required
def lista_questoes(request):
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
                    
                print(acertos + erros)
                

        user_profile.acertos += acertos
        user_profile.erros += erros
        user_profile.save()
        
        
    return redirect('lista_questoes')



def indexquestoes(request):
    return render(request, 'questoes/pages/indexquestoes.html')



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