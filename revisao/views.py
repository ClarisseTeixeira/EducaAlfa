from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render    
from .models import Flashcard, Revisao
from .forms import FlashcardForm
from datetime import date, timedelta, datetime
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from django.utils import timezone
from django.contrib import messages
from core.views.home import dashboard


# Create your views here.

@login_required
def flashcards(request):
    flashcards = Flashcard.objects.all().filter(user=request.user).order_by('-data')
    form = FlashcardForm()

    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.user = request.user
            flashcard.save()
            return redirect('flashcards')
    context = {
        "flashcards": flashcards,
        "form": form,
    }
    return render(request, 'revisao/flashcard.html', context)



@receiver(post_save, sender=Flashcard)
def revisao_inicial(sender, instance, created, **kwargs):
    if created:
        data_agendada = instance.data + timedelta(days=1)
        Revisao.objects.create(flashcard=instance, user=instance.user, data_agendada=data_agendada)


def proxima_revisao(revisao):
    if revisao.concluida:
        if revisao.flashcard.revisao_set.count() == 1:
            return revisao.data_agendada + timedelta(days=7)
        elif revisao.flashcard.revisao_set.count() == 2:
            return revisao.data_agendada + timedelta(days=8)
        elif revisao.flashcard.revisao_set.count() == 3:
            return revisao.data_agendada + timedelta(days=15)
        else:
            return revisao.data_agendada + timedelta(days=30)
    else:
        return revisao.data_agendada
    


@login_required
def detalhes_flashcard(request, id):
    user = request.user
    detalhes = get_object_or_404(Flashcard, id=id)
    revisao = Revisao.objects.filter(flashcard=detalhes, user=user, concluida=False).first()
    if not revisao:
        return HttpResponse("Você não tem permissão para acessar essa página.")


    data = timezone.now().date


    proximo = Flashcard.objects.filter(user = user, id__gt=id).order_by('id').first()
    proximo_id = proximo.id if proximo else dashboard


    anterior = Flashcard.objects.filter(user = user, id__lt=id).order_by('-id').first()
    anterior_id = anterior.id if anterior else dashboard


    if request.method == 'POST':
        if 'revisao_concluida' in request.POST:
            if revisao:
                revisao.concluida = True
                revisao.data_agendada = timezone.now().date()
                revisao.save()


                nova_data_revisao = proxima_revisao(revisao)
                Revisao.objects.create(flashcard=detalhes, user=user, data_agendada=nova_data_revisao)


                proximo_flashcard = Revisao.objects.filter(user=user, concluida=False, data_agendada__lte=timezone.now().date()).order_by('data_agendada').first()


               
                if proximo_flashcard:
                    return redirect('detalhes_flashcard', id=proximo_flashcard.flashcard.id)
                else:
                    return redirect('dashboard')
        elif 'nao_lembrou' in request.POST:  
            revisao.data_agendada = timezone.now().date() + timedelta(days=1)
            revisao.save()
           
    context = {
        'detalhes': detalhes,
        'revisao': revisao,
        'anterior_id': anterior_id,
        'proximo_id': proximo_id,
        'data': data
    }
    return render(request,'revisao/flashcard_detail.html', context)



@login_required
def calendar(request):
    user = request.user
    proximas_revisoes = Revisao.objects.filter(user=user)
    eventos = []
    for revisao in proximas_revisoes:
        eventos.append({
            'title': revisao.flashcard.titulo, 
            'start': revisao.data_agendada.strftime('%Y-%m-%d'),  
        })

    return JsonResponse(eventos, safe=False)



@login_required
def calendario(request):  
    eventos_calendario = Revisao.objects.filter(user=request.user)
    context = {
        "eventos_calendario": eventos_calendario,
    }
    return render(request, 'revisao/calendario.html', context)


@login_required
def remover(request, id):
    flashcard = get_object_or_404(Flashcard, id=id)
    flashcard.delete()
    return redirect('flashcards') 

def flashcard_editar(request, id):
    flashcard = get_object_or_404(Flashcard, id=id)

    if request.method == 'POST':
        form = FlashcardForm(request.POST, instance=flashcard)
        if form.is_valid():
            form.save()
            return redirect('flashcards')
    else:
        form = FlashcardForm(instance=flashcard)
    return render(request, 'revisao/flashcardform.html', {'form': form})



def indexrevisao(request):
    return render(request, "revisao/indexrevisao.html")