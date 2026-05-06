from datetime import timedelta

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.management.base import BaseCommand
from django.utils import timezone

from processes.models import Cliente, Movimentacao, Processo


class Command(BaseCommand):
    help = "Cria dados de exemplo para a previa local do sistema."

    def handle(self, *args, **options):
        today = timezone.localdate()
        User = get_user_model()

        advogado, _ = User.objects.get_or_create(
            username="advogado",
            defaults={
                "email": "advogado@example.com",
                "first_name": "Mariana",
                "last_name": "Costa",
            },
        )
        advogado.set_password("advogado123")
        advogado.save()

        estagiario, _ = User.objects.get_or_create(
            username="estagiario",
            defaults={
                "email": "estagiario@example.com",
                "first_name": "Lucas",
                "last_name": "Almeida",
            },
        )
        estagiario.set_password("estagio123")
        estagiario.save()

        self._add_to_group(advogado, "Advogado")
        self._add_to_group(estagiario, "Estagiario")

        clientes = [
            {
                "nome": "Construtora Horizonte Ltda",
                "cpf_cnpj": "12.345.678/0001-90",
                "contato": "juridico@horizonte.com.br",
            },
            {
                "nome": "Ana Paula Ribeiro",
                "cpf_cnpj": "123.456.789-09",
                "contato": "(11) 98888-1200",
            },
            {
                "nome": "Mercado Central Sao Bento S/A",
                "cpf_cnpj": "98.765.432/0001-10",
                "contato": "contato@saobento.example",
            },
        ]

        cliente_map = {}
        for payload in clientes:
            cliente, _ = Cliente.objects.update_or_create(
                cpf_cnpj=payload["cpf_cnpj"],
                defaults=payload,
            )
            cliente_map[payload["nome"]] = cliente

        processos = [
            {
                "numero": "1001234-56.2025.8.26.0100",
                "cliente": cliente_map["Construtora Horizonte Ltda"],
                "tribunal": "TJSP",
                "vara": "5a Vara Civel",
                "data_abertura": today - timedelta(days=120),
                "status": Processo.Status.ATIVO,
                "responsavel": advogado,
                "movimentacoes": [
                    {
                        "titulo": "Audiencia de conciliacao designada",
                        "descricao": "Audiencia marcada pelo juizo para tentativa de acordo.",
                        "data_evento": today - timedelta(days=12),
                        "prazo": today + timedelta(days=5),
                    },
                    {
                        "titulo": "Contestacao protocolada",
                        "descricao": "Peca defensiva juntada aos autos no prazo legal.",
                        "data_evento": today - timedelta(days=36),
                        "prazo": None,
                    },
                ],
            },
            {
                "numero": "0800456-22.2024.4.03.6100",
                "cliente": cliente_map["Ana Paula Ribeiro"],
                "tribunal": "TRF3",
                "vara": "2a Vara Federal",
                "data_abertura": today - timedelta(days=210),
                "status": Processo.Status.SUSPENSO,
                "responsavel": advogado,
                "movimentacoes": [
                    {
                        "titulo": "Processo suspenso por decisao interlocutoria",
                        "descricao": "Suspensao determinada ate julgamento de tema repetitivo.",
                        "data_evento": today - timedelta(days=18),
                        "prazo": None,
                    },
                ],
            },
            {
                "numero": "5007890-11.2026.8.21.0001",
                "cliente": cliente_map["Mercado Central Sao Bento S/A"],
                "tribunal": "TJRS",
                "vara": "1a Vara Empresarial",
                "data_abertura": today - timedelta(days=20),
                "status": Processo.Status.ATIVO,
                "responsavel": advogado,
                "movimentacoes": [
                    {
                        "titulo": "Prazo para replica",
                        "descricao": "Aguardando manifestacao sobre documentos juntados.",
                        "data_evento": today - timedelta(days=2),
                        "prazo": today + timedelta(days=2),
                    },
                ],
            },
        ]

        for payload in processos:
            movimentacoes = payload.pop("movimentacoes")
            processo, _ = Processo.objects.update_or_create(
                numero=payload["numero"],
                defaults=payload,
            )

            for item in movimentacoes:
                Movimentacao.objects.update_or_create(
                    processo=processo,
                    titulo=item["titulo"],
                    data_evento=item["data_evento"],
                    defaults={
                        "descricao": item["descricao"],
                        "prazo": item["prazo"],
                        "criado_por": estagiario,
                    },
                )

        self.stdout.write(self.style.SUCCESS("Dados de exemplo criados."))
        self.stdout.write("Login advogado: advogado / advogado123")
        self.stdout.write("Login estagiario: estagiario / estagio123")

    def _add_to_group(self, user, group_name):
        group = Group.objects.filter(name=group_name).first()
        if group:
            user.groups.add(group)
