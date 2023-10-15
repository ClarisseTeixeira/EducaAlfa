from django.shortcuts import render, get_object_or_404
from .models import Disciplina, Assunto, Conteudo, Materiais

def lista_disciplinas(request):
    disciplinas = Disciplina.objects.all()

    context = {
        'disciplinas': disciplinas
        }

    return render(request, 'materiais/partials/lista_disciplinas.html', context)

def lista_assuntos(request, id):    
    disciplina = get_object_or_404(Disciplina, pk=id)
    assuntos = Assunto.objects.filter(disciplina=disciplina)
    conteudos = Conteudo.objects.filter(disciplina=disciplina)
    context = {
        'disciplina': disciplina, 
        'assuntos': assuntos,
        'conteudos': conteudos
        }
    
    return render(request, 'materiais/pages/lista_assuntos.html', context) 


def lista_materiais(request, id):
    conteudo = get_object_or_404(Conteudo, pk=id)
    materiais = Materiais.objects.filter(conteudo=conteudo)
    context = {'conteudo': conteudo, 'materiais': materiais}
    return render(request, 'materiais/pages/conteudos.html', context )

