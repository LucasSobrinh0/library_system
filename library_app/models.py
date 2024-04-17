from django.db import models
from django.utils import timezone

class Cliente(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    endereco = models.TextField()

    def __str__(self):
        return self.nome

class Livro(models.Model):
    nome = models.CharField(max_length=255)
    quantidade = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.nome} (Estoque: {self.quantidade})"
    
class Emprestimo(models.Model):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE)
    livro = models.ForeignKey('Livro', on_delete=models.CASCADE)
    data_emprestimo = models.DateTimeField(default=timezone.now)
    data_devolucao = models.DateTimeField()

    def __str__(self):
        return f"{self.livro.nome} emprestado para {self.cliente.nome}"