from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def index(request):
    return render(request, 'index.html')


@login_required
def lancamentos(request):
    return render(request, 'lancamentos.html')


@login_required
def usuarios(request):
    return render(request, 'usuarios.html')


@login_required
def perfil(request):
    return render(request, 'perfil.html')


def login(request):
    return render(request, 'login.html')
