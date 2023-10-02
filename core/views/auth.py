from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout

def registro(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password_confirm = request.POST['password_confirm']

        if password == password_confirm:
            try:
                user = User.objects.create_user(username=username, password=password)
                messages.success(request, 'Usuário registrado com sucesso.')
                return redirect('login')
            except:
                messages.error(request, 'Erro ao criar usuário.')
        else:
            messages.error(request, 'As senhas não coincidem.')

    return render(request, 'registration/registro.html')

def fazer_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(index)  # Redireciona para a página inicial após o login
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def fazer_logout(request):
    if request.method == 'POST':
        logout(request)
        return redirect(index)  # Redireciona para a página inicial após o logout

def index(request):
    return render(request, 'index.html')