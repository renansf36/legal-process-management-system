from django.contrib import admin

from .models import Cliente, Documento, Movimentacao, Processo


class DocumentoInline(admin.TabularInline):
    model = Documento
    extra = 0


class MovimentacaoInline(admin.TabularInline):
    model = Movimentacao
    extra = 0


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    search_fields = ["nome", "cpf_cnpj"]
    list_display = ["nome", "cpf_cnpj", "contato"]


@admin.register(Processo)
class ProcessoAdmin(admin.ModelAdmin):
    list_display = ["numero", "cliente", "tribunal", "vara", "status"]
    list_filter = ["status", "tribunal"]
    search_fields = ["numero", "cliente__nome", "cliente__cpf_cnpj"]
    inlines = [DocumentoInline, MovimentacaoInline]


@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "processo", "enviado_por", "created_at"]
    search_fields = ["titulo", "processo__numero"]


@admin.register(Movimentacao)
class MovimentacaoAdmin(admin.ModelAdmin):
    list_display = ["titulo", "processo", "data_evento", "prazo"]
    list_filter = ["data_evento", "prazo"]
    search_fields = ["titulo", "processo__numero"]
