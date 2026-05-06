# Legal Process Management System

Sistema inicial de gestao juridica criado com Django, Bootstrap e suporte a MySQL.

## Funcionalidades

- Autenticacao com `User` nativo do Django.
- Grupos de acesso: `Admin`, `Advogado` e `Estagiario`.
- Cadastro de clientes.
- Cadastro e acompanhamento de processos.
- Historico de movimentacoes por processo.
- Upload multiplo de documentos PDF por processo.
- Dashboard com indicadores e grafico via Chart.js.
- Atualizacao de status e detalhes de processo via AJAX.
- Exportacao da lista filtrada de processos para Excel.
- Service layer mockada para futura integracao com APIs de tribunais.

## Tecnologias

- Python 3.13
- Django 5
- MySQL
- Bootstrap 5
- Chart.js
- openpyxl

## Como Rodar Localmente

Clone o repositorio e entre na pasta:

```powershell
git clone https://github.com/renansf36/legal-process-management-system.git
cd legal-process-management-system
```

Crie e ative um ambiente virtual:

```powershell
python -m venv .venv
.\\.venv\\Scripts\\Activate.ps1
```

Instale as dependencias:

```powershell
pip install -r requirements.txt
```

Copie o arquivo de ambiente:

```powershell
copy .env.example .env
```

Para desenvolvimento rapido com SQLite, altere no `.env`:

```env
DB_ENGINE=sqlite
```

Para usar MySQL, mantenha:

```env
DB_ENGINE=mysql
DB_NAME=legal_process_management
DB_USER=root
DB_PASSWORD=
DB_HOST=127.0.0.1
DB_PORT=3306
```

Crie o banco no MySQL antes de migrar:

```sql
CREATE DATABASE legal_process_management CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Execute as migracoes:

```powershell
python manage.py migrate
```

Crie um superusuario:

```powershell
python manage.py createsuperuser
```

Opcionalmente, carregue dados de exemplo:

```powershell
python manage.py seed_demo
```

Inicie o servidor:

```powershell
python manage.py runserver
```

Acesse:

```text
http://127.0.0.1:8000/login/
```

## Usuarios de Exemplo

Ao executar `python manage.py seed_demo`, os usuarios abaixo sao criados:

```text
Advogado:
usuario: advogado
senha: advogado123

Estagiario:
usuario: estagiario
senha: estagio123
```

O usuario `admin` usado na previa local nao e criado pelo seed. Para ter acesso administrativo, use `createsuperuser`.

## Estrutura Principal

```text
legal_manager/
  settings.py
  urls.py
processes/
  models.py
  forms.py
  views.py
  urls.py
  services/
    tribunal_gateway.py
templates/
static/
media/
```

## Comandos Uteis

Validar configuracao:

```powershell
python manage.py check
```

Criar novas migracoes:

```powershell
python manage.py makemigrations
```

Aplicar migracoes:

```powershell
python manage.py migrate
```

Exportar processos:

```text
Use o botao "Exportar Excel" na tela de processos.
```

## Observacoes de Producao

Antes de publicar em producao:

- Defina `DJANGO_DEBUG=False`.
- Configure uma `DJANGO_SECRET_KEY` forte.
- Configure `DJANGO_ALLOWED_HOSTS`.
- Ative HTTPS e cookies seguros.
- Configure armazenamento persistente para `MEDIA_ROOT`.
- Use credenciais reais e seguras para MySQL.
