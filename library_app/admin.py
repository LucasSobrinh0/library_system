from django.contrib import admin
from .models import Cliente, Livro, Emprestimo

admin.site.register(Cliente)
admin.site.register(Livro)
admin.site.register(Emprestimo)
