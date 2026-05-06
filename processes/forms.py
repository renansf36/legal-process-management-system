from django import forms

from .models import Cliente, Documento, Movimentacao, Processo


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            return [single_file_clean(item, initial) for item in data]
        return [single_file_clean(data, initial)]


class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ["nome", "cpf_cnpj", "contato"]


class ProcessoForm(forms.ModelForm):
    class Meta:
        model = Processo
        fields = [
            "numero",
            "tribunal",
            "vara",
            "data_abertura",
            "status",
            "cliente",
            "responsavel",
        ]
        widgets = {
            "data_abertura": forms.DateInput(attrs={"type": "date"}),
        }


class DocumentoUploadForm(forms.ModelForm):
    arquivos = MultipleFileField(
        widget=MultipleFileInput(attrs={"multiple": True, "accept": ".pdf"}),
        required=False,
        label="Arquivos PDF",
    )

    class Meta:
        model = Documento
        fields = ["titulo", "arquivos"]


class MovimentacaoForm(forms.ModelForm):
    class Meta:
        model = Movimentacao
        fields = ["titulo", "descricao", "data_evento", "prazo"]
        widgets = {
            "data_evento": forms.DateInput(attrs={"type": "date"}),
            "prazo": forms.DateInput(attrs={"type": "date"}),
        }
