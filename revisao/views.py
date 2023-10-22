from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from .models import Flashcard, Revisao
from .forms import FlashcardForm
from datetime import date, timedelta
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import ExtractWeekDay
from django.utils import timezone
from django.contrib import messages


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
    detalhes = get_object_or_404(Flashcard, id=id)
    user = request.user 

    revisao = Revisao.objects.filter(flashcard=detalhes, user=user, concluida=False).first()

    if request.method == 'POST':
        if revisao:
            revisao.concluida = True
            revisao.data_agendada = timezone.now().date()
            revisao.save()

            nova_data_revisao = proxima_revisao(revisao)
            Revisao.objects.create(flashcard=detalhes, user=user, data_agendada=nova_data_revisao)

            return redirect('detalhes_flashcard', id=detalhes.id)
    context = {
        'detalhes': detalhes,
        'revisao': revisao,
    }
    return render(request,'revisao/flashcard_detail.html' , context)




@login_required
def calendar(request):
    user = request.user
    proximas_revisoes = Revisao.objects.filter(user=user, data_agendada__gte=date.today()).order_by('data_agendada')

    eventos = []
    for revisao in proximas_revisoes:
        eventos.append({
            'title': revisao.flashcard.titulo, 
            'start': revisao.data_agendada.strftime('%Y-%m-%d'),  
        })

    return JsonResponse(eventos, safe=False)



@login_required
def calendario(request):  
    eventos_calendario = Revisao.objects.filter(user=request.user, data_agendada__gte=date.today())
    context = {
        "eventos_calendario": eventos_calendario,
    }
    return render(request, 'revisao/calendario.html', context)




@login_required
def remover(request, id):
    flashcard = get_object_or_404(Flashcard, id=id)
    flashcard.delete()
    return redirect('flashcards') 



def indexrevisao(request):
    return render(request, "revisao/indexrevisao.html")