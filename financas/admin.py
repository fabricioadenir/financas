from django.contrib import admin
from .models import Lancamento, Situacao, Usuario


class UsuarioAdmin(admin.ModelAdmin):
    model = Usuario

    list_display = [
        'nome',
        'sexo',
        'email',
        'salairo_mensal',
        'extra', 'descricao',
        'data_criacao',
        'data_modificacao'
    ]


admin.site.register(Usuario, UsuarioAdmin)


class LancamentoAdmin(admin.ModelAdmin):
    model = Lancamento

    list_display = [
        'tipo_lancamento',
        'numero_parcelas',
        'vencimento',
        'valor',
        'descricao',
        'data_criacao',
        'data_modificacao'
    ]


admin.site.register(Lancamento, LancamentoAdmin)


class SituacaoAdmin(admin.ModelAdmin):
    model = Situacao

    list_display = [
        'mes_corrente',
        'valor_total_arrecadado',
        'valor_total_pago',
        'valor_total_disponivel',
        'situacao',
        'data_criacao',
        'data_modificacao'
    ]


admin.site.register(Situacao, SituacaoAdmin)
