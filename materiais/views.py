from django.shortcuts import render, get_object_or_404, redirect
from .models import Disciplina, Assunto, Conteudo, Materiais
from django.contrib import messages
from .forms import DisciplinaForm, AssuntoForm, ConteudoForm, MateriaisForm
from django.contrib.auth.decorators import user_passes_test
from core.views.auth import superuser
from core.views.home import arearestrita

def lista_disciplinas(request):
    disciplinas = Disciplina.objects.all()

    context = {
        'disciplinas': disciplinas
        }

    return render(request, 'materiais/lista_disciplinas.html', context)

def lista_assuntos(request, id):    
    disciplina = get_object_or_404(Disciplina, pk=id)
    assuntos = Assunto.objects.filter(disciplina=disciplina)
    conteudos = Conteudo.objects.filter(disciplina=disciplina)
    context = {
        'disciplina': disciplina, 
        'assuntos': assuntos,
        'conteudos': conteudos
        }
    
    return render(request, 'materiais/lista_assuntos.html', context) 


def lista_materiais(request, id):
    conteudo = get_object_or_404(Conteudo, pk=id)
    materiais = Materiais.objects.filter(conteudo=conteudo)

    context = {
        'conteudo': conteudo, 
        'materiais': materiais
        }
    return render(request, 'materiais/conteudos.html', context )


@user_passes_test(superuser)
def disciplina_criar(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Disciplina criada com sucesso!')
            form = DisciplinaForm()
    else:
        form = DisciplinaForm()

    return render(request, "materiais/forms/formdisciplina.html", {'form': form})


@user_passes_test(superuser)
def assunto_criar(request):
    if request.method == 'POST':
        form = AssuntoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Assunto criado com sucesso!')
            form = AssuntoForm()
    else:
        form = AssuntoForm()

    return render(request, "materiais/forms/formassunto.html", {'form': form})

@user_passes_test(superuser)
def conteudo_criar(request):
    if request.method == 'POST':
        form = ConteudoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conteúdo criado com sucesso!')
            form = ConteudoForm()
    else:
        form = ConteudoForm()

    return render(request, "materiais/forms/formconteudo.html", {'form': form})


@user_passes_test(superuser)
def materiais_criar(request):
    if request.method == 'POST':
        form = MateriaisForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Materiais criados com sucesso!')
            form = MateriaisForm()
    else:
        form = MateriaisForm()

    return render(request, "materiais/forms/formmateriais.html", {'form': form})


def materiais_remover(request, id):
    material = get_object_or_404(Materiais, id=id)
    material.delete()
    messages.success(request, 'Material excluído com sucesso!')
    return redirect('arearestrita')

def assunto_remover(request, id):
    assunto = get_object_or_404(Assunto, id=id)
    assunto.delete()
    return redirect('arearestrita')

def disciplina_remover(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)
    disciplina.delete()
    messages.success(request, 'Disciplina excluída com sucesso!')
    return redirect('arearestrita')

def conteudo_remover(request, id):
    conteudo = get_object_or_404(Conteudo, id=id)
    conteudo.delete()
    return redirect('arearestrita')



def materiais_editar(request, id):
    material = get_object_or_404(Materiais, id=id)
    if request.method == 'POST':
        form = MateriaisForm(request.POST, request.FILES, instance=material)
        if form.is_valid():
            form.save()
            return redirect('materiais_listar')
    else:
        form = MateriaisForm(instance=material)
    return render(request, 'materiais/forms/formmateriais.html', {'form': form})

def assunto_editar(request, id):
    assunto = get_object_or_404(Assunto, id=id)
    if request.method == 'POST':
        form = AssuntoForm(request.POST, instance=assunto)
        if form.is_valid():
            form.save()
            return redirect('assunto_listar')
    else:
        form = AssuntoForm(instance=assunto)
    return render(request, 'materiais/forms/formassunto.html', {'form': form})

def disciplina_editar(request, id):
    disciplina = get_object_or_404(Disciplina, id=id)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            return redirect('disciplina_listar')
    else:
        form = DisciplinaForm(instance=disciplina)
    return render(request, 'materiais/forms/formdisciplina.html', {'form': form})

def conteudo_editar(request, id):
    conteudo = get_object_or_404(Conteudo, id=id)
    if request.method == 'POST':
        form = ConteudoForm(request.POST, instance=conteudo)
        if form.is_valid():
            form.save()
            return redirect('conteudo_listar')
    else:
        form = ConteudoForm(instance=conteudo)
    return render(request, 'materiais/forms/formconteudo.html', {'form': form})
