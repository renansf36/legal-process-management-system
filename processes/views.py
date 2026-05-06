from datetime import timedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Count, Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import View
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    TemplateView,
    UpdateView,
)
from openpyxl import Workbook

from .forms import ClienteForm, DocumentoUploadForm, MovimentacaoForm, ProcessoForm
from .models import Cliente, Documento, Movimentacao, Processo
from .services.tribunal_gateway import MockTribunalGateway


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "processes/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.localdate()
        next_week = today + timedelta(days=7)

        status_counts = (
            Processo.objects.values("status")
            .annotate(total=Count("id"))
            .order_by("status")
        )

        context.update(
            {
                "processos_ativos": Processo.objects.filter(
                    status=Processo.Status.ATIVO
                ).count(),
                "prazos_proximos": Movimentacao.objects.filter(
                    prazo__gte=today,
                    prazo__lte=next_week,
                ).count(),
                "clientes_total": Cliente.objects.count(),
                "movimentacoes_recentes": Movimentacao.objects.select_related(
                    "processo"
                )[:6],
                "chart_labels": [
                    Processo.Status(item["status"]).label for item in status_counts
                ],
                "chart_values": [item["total"] for item in status_counts],
            }
        )
        return context


class ClienteListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Cliente
    permission_required = "processes.view_cliente"
    paginate_by = 20
    template_name = "processes/cliente_list.html"

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")
        if query:
            queryset = queryset.filter(
                Q(nome__icontains=query) | Q(cpf_cnpj__icontains=query)
            )
        return queryset


class ClienteDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Cliente
    permission_required = "processes.view_cliente"
    template_name = "processes/cliente_detail.html"


class ClienteCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    permission_required = "processes.add_cliente"
    template_name = "processes/form.html"


class ClienteUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    permission_required = "processes.change_cliente"
    template_name = "processes/form.html"


class ClienteDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Cliente
    permission_required = "processes.delete_cliente"
    success_url = reverse_lazy("cliente_list")
    template_name = "processes/confirm_delete.html"


class ProcessoListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Processo
    permission_required = "processes.view_processo"
    paginate_by = 20
    template_name = "processes/processo_list.html"

    def get_queryset(self):
        queryset = super().get_queryset().select_related("cliente", "responsavel")
        status = self.request.GET.get("status")
        query = self.request.GET.get("q")

        if status:
            queryset = queryset.filter(status=status)
        if query:
            queryset = queryset.filter(
                Q(numero__icontains=query)
                | Q(cliente__nome__icontains=query)
                | Q(tribunal__icontains=query)
            )
        return queryset


class ProcessoDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Processo
    permission_required = "processes.view_processo"
    template_name = "processes/processo_detail.html"

    def get_queryset(self):
        return super().get_queryset().select_related("cliente", "responsavel")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["document_form"] = DocumentoUploadForm()
        context["movimentacao_form"] = MovimentacaoForm()
        context["tribunal_snapshot"] = MockTribunalGateway().buscar_processo(
            self.object.numero
        )
        return context


class ProcessoCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Processo
    form_class = ProcessoForm
    permission_required = "processes.add_processo"
    template_name = "processes/form.html"


class ProcessoUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Processo
    form_class = ProcessoForm
    permission_required = "processes.change_processo"
    template_name = "processes/form.html"


class ProcessoDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Processo
    permission_required = "processes.delete_processo"
    success_url = reverse_lazy("processo_list")
    template_name = "processes/confirm_delete.html"


class DocumentoUploadView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "processes.add_documento"

    def post(self, request, pk):
        processo = get_object_or_404(Processo, pk=pk)
        form = DocumentoUploadForm(request.POST, request.FILES)

        if not form.is_valid():
            messages.error(request, "Verifique os dados do upload.")
            return redirect(processo)

        titulo = form.cleaned_data["titulo"]
        files = request.FILES.getlist("arquivos")
        for uploaded_file in files:
            Documento.objects.create(
                processo=processo,
                titulo=titulo or uploaded_file.name,
                arquivo=uploaded_file,
                enviado_por=request.user,
            )

        messages.success(request, f"{len(files)} documento(s) enviado(s).")
        return redirect(processo)


class MovimentacaoCreateAjaxView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "processes.add_movimentacao"

    def post(self, request, pk):
        processo = get_object_or_404(Processo, pk=pk)
        form = MovimentacaoForm(request.POST)

        if not form.is_valid():
            return JsonResponse({"ok": False, "errors": form.errors}, status=400)

        movimentacao = form.save(commit=False)
        movimentacao.processo = processo
        movimentacao.criado_por = request.user
        movimentacao.save()

        return JsonResponse(
            {
                "ok": True,
                "movimentacao": {
                    "titulo": movimentacao.titulo,
                    "data_evento": movimentacao.data_evento.isoformat(),
                    "prazo": movimentacao.prazo.isoformat()
                    if movimentacao.prazo
                    else "",
                },
            }
        )


class ProcessoStatusAjaxView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "processes.can_update_status"

    def post(self, request, pk):
        processo = get_object_or_404(Processo, pk=pk)
        status = request.POST.get("status")
        valid_statuses = dict(Processo.Status.choices)

        if status not in valid_statuses:
            return JsonResponse({"ok": False, "error": "Status invalido."}, status=400)

        processo.status = status
        processo.save(update_fields=["status", "updated_at"])
        return JsonResponse(
            {"ok": True, "status": status, "label": processo.get_status_display()}
        )


class ProcessoDetailAjaxView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "processes.view_processo"

    def get(self, request, pk):
        processo = get_object_or_404(
            Processo.objects.select_related("cliente", "responsavel"),
            pk=pk,
        )
        return JsonResponse(
            {
                "numero": processo.numero,
                "cliente": processo.cliente.nome,
                "tribunal": processo.tribunal,
                "vara": processo.vara,
                "status": processo.get_status_display(),
                "responsavel": processo.responsavel.get_full_name()
                if processo.responsavel
                else "",
            }
        )


class ProcessoExportView(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = "processes.can_export_processos"

    def get(self, request):
        queryset = ProcessoListView()
        queryset.request = request
        processos = queryset.get_queryset()

        workbook = Workbook()
        worksheet = workbook.active
        worksheet.title = "Processos"
        worksheet.append(
            [
                "Numero",
                "Cliente",
                "CPF/CNPJ",
                "Tribunal",
                "Vara",
                "Data de abertura",
                "Status",
                "Responsavel",
            ]
        )

        for processo in processos:
            worksheet.append(
                [
                    processo.numero,
                    processo.cliente.nome,
                    processo.cliente.cpf_cnpj,
                    processo.tribunal,
                    processo.vara,
                    processo.data_abertura.isoformat(),
                    processo.get_status_display(),
                    processo.responsavel.get_full_name()
                    if processo.responsavel
                    else "",
                ]
            )

        response = HttpResponse(
            content_type=(
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        )
        response["Content-Disposition"] = 'attachment; filename="processos.xlsx"'
        workbook.save(response)
        return response
