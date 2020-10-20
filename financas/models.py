from django.db import models
from datetime import datetime
from partial_date import PartialDate, PartialDateField
from .regras_situacoes import regras


class Usuario(models.Model):
    SEXO = (
        (u'f', u'Feminino'),
        (u'm', u'Masculino'),
    )
    nome = models.CharField(max_length=250, verbose_name='Nome ')
    sexo = models.CharField(
        max_length=1, choices=SEXO, verbose_name='Sexo ')
    email = models.EmailField(verbose_name='E-mail ')
    salairo_mensal = models.FloatField(verbose_name='Salário ')
    extra = models.FloatField(blank=True, null=True, verbose_name='Extra ', default=0)
    descricao = models.TextField(blank=True, verbose_name='Descição do extra ')
    data_criacao = models.DateTimeField(
        verbose_name='Data criação ', editable=False, auto_now_add=True)
    data_modificacao = models.DateTimeField(
        verbose_name='Data modificação ', editable=False, auto_now=True)

    def __str__(self):
        return self.nome

    class Meta:
        verbose_name_plural = "1-Usuários"


class Lancamento(models.Model):
    TIPO_LANCAMENTO = (
        (u'd', u'Gasto dia dia'),
        (u'm', u'Gasto Mensal'),
        (u'p', u'Gasto Programada'),
        (u'e', u'Dinheiro extra'),
    )
    # mes_calculo = models.DateField(blank=True, null=True, verbose_name='Mês Calculo ')
    tipo_lancamento = models.CharField(
        max_length=1, choices=TIPO_LANCAMENTO, verbose_name='Tipo lançamento ')
    numero_parcelas = models.IntegerField(blank=True, null=True, verbose_name="Quantas vezes ")
    vencimento = models.DateField(blank=True, null=True, verbose_name='Vencimento ')
    valor = models.FloatField(verbose_name='Valor ')
    descricao = models.TextField(blank=True, null=True, verbose_name='Descição do extra ')
    data_criacao = models.DateTimeField(
        primary_key=True,
        verbose_name='Data criação ', editable=False, auto_now_add=True)
    data_modificacao = models.DateTimeField(
        verbose_name='Data modificação ', editable=False, auto_now=True)

    def __str__(self):
        return f"{self.get_tipo_lancamento_display()} R$: {self.valor} Descrição: {self.descricao}"

    def save(self, *args, **kwargs):
        data_mes_ano = datetime.now().strftime('%Y-%m')
        data = PartialDate(data_mes_ano)

        soma_salario_e_extras = 0
        valor_a_pagar = 0

        super(Lancamento, self).save(*args, **kwargs)
        situacao = Situacao.objects.filter(mes_corrente=data)

        lancamento = Lancamento.objects.get(pk=self.pk)
        if situacao:
            for item in situacao:
                if self.tipo_lancamento == 'e':
                    item.valor_total_disponivel += self.valor
                else:
                    item.valor_total_pago += self.valor
                    item.valor_total_disponivel -= self.valor
                status = regras.get_status(item.valor_total_disponivel)
                item.situacao = status
                item.save()
                item.lancamentos.add(lancamento)

        else:
            usuarios = Usuario.objects.all()
            for usuario in usuarios:
                soma_salario_e_extras += usuario.salairo_mensal + usuario.extra
            soma_salario_e_extras = 0
            usuarios = Usuario.objects.all()
            for usuario in usuarios:
                soma_salario_e_extras += usuario.salairo_mensal + usuario.extra
            if self.tipo_lancamento == 'e':
                soma_salario_e_extras += self.valor
            else:
                valor_a_pagar = self.valor

            disponivel = soma_salario_e_extras - valor_a_pagar

            status = regras.get_status(item.valor_total_disponivel)

            situacao = Situacao(
                situacao=status,
                mes_corrente=data,
                valor_total_arrecadado=soma_salario_e_extras,
                valor_total_pago=valor_a_pagar,
                valor_total_disponivel=disponivel
            )
            situacao.save()
            situacao.lancamentos.add(lancamento)

    class Meta:
        verbose_name_plural = "2-Lançamentos"


class Situacao(models.Model):
    SITUACAO = (
        (u'p', u'Positivo'),
        (u'n', u'Negativo'),
        (u'l', u'No Limite'),
    )
    valor_total_arrecadado = models.FloatField(verbose_name='Valor total recebido ')
    valor_total_pago = models.FloatField(verbose_name='Valor total pago/apagar ')
    lancamentos = models.ManyToManyField(Lancamento, verbose_name="Lançamentos ")
    valor_total_disponivel = models.FloatField(verbose_name='Valor total disponível ')
    situacao = models.CharField(
        max_length=1, choices=SITUACAO, verbose_name='Situação ')
    mes_corrente = PartialDateField(primary_key=True, verbose_name="Mês de calculo ")
    data_criacao = models.DateTimeField(
        verbose_name='Data criação ', editable=False, auto_now_add=True)
    data_modificacao = models.DateTimeField(
        verbose_name='Data modificação ', editable=False, auto_now=True)

    class Meta:
        verbose_name_plural = "3-Situaçôes"
