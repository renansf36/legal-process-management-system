from django.urls import path

from . import views


urlpatterns = [
    path("", views.DashboardView.as_view(), name="dashboard"),
    path("clientes/", views.ClienteListView.as_view(), name="cliente_list"),
    path("clientes/novo/", views.ClienteCreateView.as_view(), name="cliente_create"),
    path("clientes/<int:pk>/", views.ClienteDetailView.as_view(), name="cliente_detail"),
    path(
        "clientes/<int:pk>/editar/",
        views.ClienteUpdateView.as_view(),
        name="cliente_update",
    ),
    path(
        "clientes/<int:pk>/excluir/",
        views.ClienteDeleteView.as_view(),
        name="cliente_delete",
    ),
    path("processos/", views.ProcessoListView.as_view(), name="processo_list"),
    path("processos/novo/", views.ProcessoCreateView.as_view(), name="processo_create"),
    path(
        "processos/exportar/",
        views.ProcessoExportView.as_view(),
        name="processo_export",
    ),
    path(
        "processos/<int:pk>/",
        views.ProcessoDetailView.as_view(),
        name="processo_detail",
    ),
    path(
        "processos/<int:pk>/editar/",
        views.ProcessoUpdateView.as_view(),
        name="processo_update",
    ),
    path(
        "processos/<int:pk>/excluir/",
        views.ProcessoDeleteView.as_view(),
        name="processo_delete",
    ),
    path(
        "processos/<int:pk>/documentos/",
        views.DocumentoUploadView.as_view(),
        name="documento_upload",
    ),
    path(
        "processos/<int:pk>/movimentacoes/ajax/",
        views.MovimentacaoCreateAjaxView.as_view(),
        name="movimentacao_create_ajax",
    ),
    path(
        "processos/<int:pk>/status/ajax/",
        views.ProcessoStatusAjaxView.as_view(),
        name="processo_status_ajax",
    ),
    path(
        "processos/<int:pk>/detalhes/ajax/",
        views.ProcessoDetailAjaxView.as_view(),
        name="processo_detail_ajax",
    ),
]
