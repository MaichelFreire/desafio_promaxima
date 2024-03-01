from django.db import models



class DataSerch(models.Model):

    descricao_licitacao = models.TextField()
    n_certame = models.TextField()
    atividade = models.TextField()
    modalidade = models.TextField()
    comprador = models.TextField()
    descricao = models.TextField()
    unidade = models.TextField()
    quantidade = models.IntegerField()
    valor = models.FloatField()
    data_inclusao = models.DateTimeField(auto_now_add=True)

    def __str__(self):

        return self.descricao_licitacao