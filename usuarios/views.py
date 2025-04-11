from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth import authenticate, login, logout


# Removed redundant definition of the `cadastro` function
    
def cadastro(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "GET":
        return render(request, 'cadastro.html')
    else:
        primeiro_nome = request.POST.get('primeiro_nome')
        ultimo_nome = request.POST.get('ultimo_nome')
        username = request.POST.get('username')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar_senha')
        messages.add_message(request, constants.ERROR, 'As senhas não coincidem')


        if not senha == confirmar_senha:    
            return redirect('cadastro')
        
        if len(senha) < 6:
            return redirect('cadastro')
        
        try:
            # Username deve ser único!
            User.objects.create_user(
                first_name=primeiro_nome,
                last_name=ultimo_nome,
                username=username,
                email=email,
                password=senha,
            )
        except Exception as e:
            messages.add_message(request, constants.ERROR, f'Erro ao criar usuário: {e}')
            return redirect('cadastro')


        return redirect('cadastro')
    

def logar(request):
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        username = request.POST.get('username')
        senha = request.POST.get('senha')

        user = authenticate(username=username, password=senha)

        if user:
            login(request, user)
						
            return redirect('/')
        else:
            messages.add_message(request, constants.ERROR, 'Usuario ou senha inválidos')
            return redirect('login')
        
def home(request):
    
    if request.user.is_authenticated:
        nome = request.user.first_name
        return render(request, 'home.html', {'nome': nome})
    
    return render(request, 'home.html')

def sair(request):
    logout(request)
    return redirect('/')