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
def form_flashcard(request):
    if request.method == 'POST':
        form = FlashcardForm(request.POST)
        if form.is_valid():
            flashcard = form.save(commit=False)
            flashcard.user = request.user  
            flashcard.save()
            messages.success(request, 'Flashcard criado com sucesso.')
            return
    else:
        form = FlashcardForm()
          
    return render(request, 'revisao/form_flashcard.html', {'form': form})


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
def detalhes_flashcard(request, flashcard_id):
    flashcard = get_object_or_404(Flashcard, id=flashcard_id)
    user = request.user 

    revisao = Revisao.objects.filter(flashcard=flashcard, user=user, concluida=False).first()

    if request.method == 'POST':
        if revisao:
            revisao.concluida = True
            revisao.data_agendada = timezone.now().date()
            revisao.save()

            nova_data_revisao = proxima_revisao(revisao)
            Revisao.objects.create(flashcard=flashcard, user=user, data_agendada=nova_data_revisao)

            return redirect('detalhes_flashcard', flashcard_id=flashcard.id)
    context = {
        'flashcard': flashcard,
        'revisao': revisao,
    }
    return render(request,'revisao/flashcard_detail.html'  , context)




@login_required 
def lista_revisao(request):
    user = request.user 

    todas_revisoes = Revisao.objects.filter(user=user, data_agendada__gte=date.today()).order_by('data_agendada')

    revisoes_do_dia = Revisao.objects.filter(user=user, data_agendada=date.today(), concluida=False)

    revisoes_pendentes = Revisao.objects.filter(user=user, data_agendada__lt=date.today(), concluida=False)

    context = {
        'todas_revisoes': todas_revisoes,
        'revisoes_do_dia': revisoes_do_dia,
        'revisoes_pendentes': revisoes_pendentes,
    }
    return render(request, 'revisao/calendar.html', context)


@login_required
def calendario(request):
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
def revisoes_por_dia_da_semana(request):
    user = request.user
    today = timezone.now().date()
    start_date = today - timedelta(days=6)

    revisoes = Revisao.objects.filter(
        user=user,
        concluida=True,
        data_agendada__range=[start_date, today]
    ).annotate(
        dia_semana=ExtractWeekDay('data_agendada')
    ).values('dia_semana').annotate(total=Count('id')).order_by('dia_semana')

    dias_da_semana = [0] * 7
    nomes_dias_semana = []

    for revisao in revisoes:
        dia_semana = revisao['dia_semana'] 
        dias_da_semana[dia_semana] = revisao['total']

    # Defina rótulos para os dias da semana na ordem desejada
    dias_semana_ordem = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo' ]
    
    dia_atual_idx = today.weekday()

    nomes_dias_semana = dias_semana_ordem[dia_atual_idx + 1:] + dias_semana_ordem[:dia_atual_idx + 1]

    return render(request, 'revisao/revisoes_por_dia_da_semana.html', {
        'dias_da_semana': dias_da_semana,
        'nomes_dias_semana': nomes_dias_semana,
    })





@login_required
def tudo(request):  
    flashcards = Flashcard.objects.all()
    eventos_calendario = []

    context = {
        "flashcards": flashcards,
        "eventos_calendario": eventos_calendario,
    }
    return render(request, 'revisao/calendar.html', context)