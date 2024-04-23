from django.urls import path
from .views import login_view, logout_view, clientes, novo_cliente, editar_cliente, remover_cliente, cadastrar_livro, lista_livros, emprestar_livro, realizar_emprestimo, controle_emprestimos, editar_emprestimo, remover_emprestimo, remover_livro, exportar_clientes_csv, exportar_clientes_excel, exportar_livros_csv, exportar_livros_excel, exportar_emprestimos_csv, exportar_emprestimos_excel

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('clientes/', clientes, name='lista_clientes'),
    path('cliente/novo/', novo_cliente, name='novo_cliente'),
    path('cliente/editar/<int:id>/', editar_cliente, name='editar_cliente'),
    path('cliente/remover/<int:id>/', remover_cliente, name='remover_cliente'),
    path('livro/novo/', cadastrar_livro, name='cadastrar_livro'),
    path('livros/', lista_livros, name='lista_livros'),
    path('livro/emprestar/', emprestar_livro, name='emprestar_livro'),
    path('emprestimo/realizar/<int:cliente_id>/', realizar_emprestimo, name='realizar_emprestimo'),
    path('emprestimos/', controle_emprestimos, name='controle_emprestimos'),
    path('emprestimo/editar/<int:emprestimo_id>/', editar_emprestimo, name='editar_emprestimo'),
    path('emprestimo/remover/<int:emprestimo_id>/', remover_emprestimo, name='remover_emprestimo'),
    path('livro/remover/<int:id>/', remover_livro, name='remover_livro'),
    path('clientes/export/csv/', exportar_clientes_csv, name='exportar_clientes_csv'),
    path('clientes/export/excel/', exportar_clientes_excel, name='exportar_clientes_excel'),
    path('livros/export/csv/', exportar_livros_csv, name='exportar_livros_csv'),
    path('livros/export/excel/', exportar_livros_excel, name='exportar_livros_excel'),
    path('emprestimo/expor/csv', exportar_emprestimos_csv, name='exportar_emprestimos_csv'),
    path('emprestimo/expor/excel', exportar_emprestimos_excel, name='exportar_emprestimos_excel')
]
