from django.contrib.auth.models import Group, Permission
from django.db.models.signals import post_migrate
from django.dispatch import receiver


ROLE_PERMISSIONS = {
    "Admin": [
        "add_cliente",
        "change_cliente",
        "delete_cliente",
        "view_cliente",
        "add_processo",
        "change_processo",
        "delete_processo",
        "view_processo",
        "can_export_processos",
        "can_update_status",
        "add_documento",
        "change_documento",
        "delete_documento",
        "view_documento",
        "add_movimentacao",
        "change_movimentacao",
        "delete_movimentacao",
        "view_movimentacao",
    ],
    "Advogado": [
        "add_cliente",
        "change_cliente",
        "view_cliente",
        "add_processo",
        "change_processo",
        "view_processo",
        "can_export_processos",
        "can_update_status",
        "add_documento",
        "view_documento",
        "add_movimentacao",
        "change_movimentacao",
        "view_movimentacao",
    ],
    "Estagiario": [
        "view_cliente",
        "view_processo",
        "add_documento",
        "view_documento",
        "add_movimentacao",
        "view_movimentacao",
    ],
}


@receiver(post_migrate)
def create_access_groups(sender, **kwargs):
    for group_name, codenames in ROLE_PERMISSIONS.items():
        group, _ = Group.objects.get_or_create(name=group_name)
        permissions = Permission.objects.filter(codename__in=codenames)
        group.permissions.set(permissions)
