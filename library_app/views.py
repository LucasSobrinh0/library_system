from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import Cliente
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Livro, Emprestimo
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('lista_clientes')
        else:
            return render(request, 'login.html', {'error': 'Login inválido.'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes.html', {'clientes': clientes})

@login_required
def novo_cliente(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        endereco = request.POST.get('endereco')
        Cliente.objects.create(nome=nome, email=email, endereco=endereco)
        return redirect('lista_clientes')
    return render(request, 'novo_cliente.html')

@login_required
def editar_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    if request.method == 'POST':
        cliente.nome = request.POST.get('nome')
        cliente.email = request.POST.get('email')
        cliente.endereco = request.POST.get('endereco')
        cliente.save()
        return redirect('lista_clientes')
    return render(request, 'editar_cliente.html', {'cliente': cliente})

@login_required
def remover_cliente(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.delete()
    return redirect('lista_clientes')

@login_required
def cadastrar_livro(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        quantidade = request.POST.get('quantidade', 0)
        Livro.objects.create(nome=nome, quantidade=quantidade)
        return redirect('lista_livros')
    return render(request, 'cadastrar_livro.html')

@login_required
def lista_livros(request):
    livros = Livro.objects.all()
    return render(request, 'lista_livros.html', {'livros': livros})

@login_required
def emprestar_livro(request):
    if request.method == 'GET' and 'query' in request.GET:
        query = request.GET.get('query')
        clientes = Cliente.objects.filter(Q(nome__icontains=query) | Q(email__icontains=query))
    else:
        clientes = Cliente.objects.all()
    livros = Livro.objects.filter(quantidade__gt=0)
    return render(request, 'emprestar_livro.html', {'clientes': clientes, 'livros': livros})


@login_required
def realizar_emprestimo(request, cliente_id):
    cliente = get_object_or_404(Cliente, id=cliente_id)
    if request.method == 'POST':
        livro_id = request.POST.get('livro')
        data_devolucao = request.POST.get('data_devolucao')
        livro = get_object_or_404(Livro, id=livro_id)
        if livro.quantidade > 0:
            livro.quantidade -= 1
            livro.save()
            Emprestimo.objects.create(cliente=cliente, livro=livro, data_devolucao=data_devolucao)
        return redirect('controle_emprestimos')
    return HttpResponse("Método não permitido", status=405)

@login_required
def controle_emprestimos(request):
    emprestimos = Emprestimo.objects.all().order_by('-data_emprestimo')
    return render(request, 'controle_emprestimos.html', {'emprestimos': emprestimos})

@login_required
def editar_emprestimo(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id)
    if request.method == 'POST':
        data_devolucao = request.POST.get('data_devolucao')
        data_devolucao_date = datetime.datetime.strptime(data_devolucao, '%Y-%m-%d').date()

        if data_devolucao_date < emprestimo.data_emprestimo.date():
            return HttpResponse("A data de devolução não pode ser anterior à data de emprestimo.", status=400)

        emprestimo.data_devolucao = data_devolucao
        emprestimo.save()
        return redirect('controle_emprestimos')
    
    return render(request, 'editar_emprestimo.html', {'emprestimo': emprestimo})

@login_required
def remover_emprestimo(request, emprestimo_id):
    emprestimo = get_object_or_404(Emprestimo, id=emprestimo_id)
    emprestimo.delete()
    return redirect('controle_emprestimos')

@login_required
def remover_livro(request, id):
    livro = get_object_or_404(Livro, id=id)
    livro.delete()
    return redirect('lista_livros')