from django.conf import settings
from django.db import models
from django.urls import reverse


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Cliente(TimeStampedModel):
    nome = models.CharField(max_length=180)
    cpf_cnpj = models.CharField("CPF/CNPJ", max_length=20, unique=True)
    contato = models.CharField(max_length=180, blank=True)

    class Meta:
        ordering = ["nome"]
        verbose_name = "cliente"
        verbose_name_plural = "clientes"

    def __str__(self):
        return self.nome

    def get_absolute_url(self):
        return reverse("cliente_detail", kwargs={"pk": self.pk})


class Processo(TimeStampedModel):
    class Status(models.TextChoices):
        ATIVO = "ativo", "Ativo"
        SUSPENSO = "suspenso", "Suspenso"
        ARQUIVADO = "arquivado", "Arquivado"
        ENCERRADO = "encerrado", "Encerrado"

    numero = models.CharField("numero do processo", max_length=40, unique=True)
    tribunal = models.CharField(max_length=120)
    vara = models.CharField(max_length=120)
    data_abertura = models.DateField()
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ATIVO,
    )
    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.PROTECT,
        related_name="processos",
    )
    responsavel = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processos_responsavel",
    )

    class Meta:
        ordering = ["-data_abertura", "numero"]
        permissions = [
            ("can_export_processos", "Pode exportar processos"),
            ("can_update_status", "Pode atualizar status do processo"),
        ]
        verbose_name = "processo"
        verbose_name_plural = "processos"

    def __str__(self):
        return self.numero

    def get_absolute_url(self):
        return reverse("processo_detail", kwargs={"pk": self.pk})


class Documento(TimeStampedModel):
    processo = models.ForeignKey(
        Processo,
        on_delete=models.CASCADE,
        related_name="documentos",
    )
    titulo = models.CharField(max_length=180)
    arquivo = models.FileField(upload_to="documentos/%Y/%m/")
    enviado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="documentos_enviados",
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "documento"
        verbose_name_plural = "documentos"

    def __str__(self):
        return self.titulo


class Movimentacao(TimeStampedModel):
    processo = models.ForeignKey(
        Processo,
        on_delete=models.CASCADE,
        related_name="movimentacoes",
    )
    titulo = models.CharField(max_length=180)
    descricao = models.TextField()
    data_evento = models.DateField()
    prazo = models.DateField(null=True, blank=True)
    criado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="movimentacoes_criadas",
    )

    class Meta:
        ordering = ["-data_evento", "-created_at"]
        verbose_name = "movimentacao"
        verbose_name_plural = "movimentacoes"

    def __str__(self):
        return f"{self.processo} - {self.titulo}"
