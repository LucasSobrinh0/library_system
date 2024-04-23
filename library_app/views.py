from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Cliente, Livro, Emprestimo
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required, user_passes_test
import datetime
import pandas as pd
import csv

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

@login_required
def exportar_clientes_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="clientes.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'Email', 'Endereço'])

    clientes = Cliente.objects.all()
    for cliente in clientes:
        writer.writerow([cliente.nome, cliente.email, cliente.endereco])

    return response


@login_required
def exportar_clientes_excel(request):
    # Criar um DataFrame pandas
    data = list(Cliente.objects.all().values("nome", "email", "endereco"))
    df = pd.DataFrame(data)

    # Criar uma resposta do tipo Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="clientes.xlsx"'

    # Escrever o DataFrame para um arquivo Excel
    with pd.ExcelWriter(response) as writer:
        df.to_excel(writer, index=False, sheet_name='Clientes')

    return response

@login_required
def exportar_livros_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="estoque_livros.csv"'

    writer = csv.writer(response)
    writer.writerow(['Nome', 'Quantidade'])

    livros = Livro.objects.all()
    for livro in livros:
        writer.writerow([livro.nome, livro.quantidade])

    return response

@login_required
def exportar_livros_excel(request):
    data = list(Livro.objects.all().values('nome', 'quantidade'))
    df = pd.DataFrame(data)

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="estoque_livros.xlsx"'

    with pd.ExcelWriter(response) as writer:
        df.to_excel(writer, index=False, sheet_name='estoque_livros')

    return response

@login_required
def exportar_emprestimos_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="lista_de_emprestimos.csv"'

    writer = csv.writer(response)
    writer.writerow(['Cliente', 'Livro', 'Data Emprestimo', 'Data devolucao'])

    emprestimos = Emprestimo.objects.all()
    for emprestimo in emprestimos:
        writer.writerow([emprestimo.cliente, emprestimo.livro, emprestimo.data_emprestimo, emprestimo.data_devolucao])

    return response

@login_required
def exportar_emprestimos_excel(request):
    # Buscando empréstimos e relacionando com Cliente e Livro para acesso direto aos campos necessários
    emprestimos = Emprestimo.objects.select_related('cliente', 'livro')

    # Preparando os dados para exportação
    data = [{
        'Cliente': emp.cliente.nome,
        'Livro': emp.livro.nome,
        'Data de Empréstimo': emp.data_emprestimo.strftime('%Y-%m-%d %H:%M'),  # Formatando data e hora
        'Data de Devolução': emp.data_devolucao.strftime('%Y-%m-%d %H:%M')
    } for emp in emprestimos]

    # Criando DataFrame do pandas
    df = pd.DataFrame(data)

    # Configurando a resposta HTTP para formato Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        headers={'Content-Disposition': 'attachment; filename="lista_de_emprestimos.xlsx"'},
    )

    # Escrevendo o DataFrame para o arquivo Excel
    with pd.ExcelWriter(response) as writer:
        df.to_excel(writer, index=False, sheet_name='Lista de Empréstimos')

    return response