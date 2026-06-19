from __future__ import annotations

from django.db import migrations

# Baseline permissions for a regular user: CRUD own tasks + self-account CRUD
# (no add_user; account creation is signup). See docs/threat-model/access-control.md.
GROUP_NAME = "users"
PERM_CODENAMES = [
    "add_task",
    "change_task",
    "delete_task",
    "view_task",
    "view_user",
    "change_user",
    "delete_user",
]


def create_default_group(apps, schema_editor):
    # Ensure the auto-created model permissions exist before we assign them.
    from django.apps import apps as global_apps
    from django.contrib.auth.management import create_permissions

    for app_label in ("tasks", "users"):
        create_permissions(
            global_apps.get_app_config(app_label),
            apps=global_apps,
            verbosity=0,
        )

    Group = apps.get_model("auth", "Group")
    Permission = apps.get_model("auth", "Permission")

    group, _ = Group.objects.get_or_create(name=GROUP_NAME)
    perms = Permission.objects.filter(
        codename__in=PERM_CODENAMES,
        content_type__app_label__in=("tasks", "users"),
    )
    group.permissions.set(perms)


def remove_default_group(apps, schema_editor):
    Group = apps.get_model("auth", "Group")
    Group.objects.filter(name=GROUP_NAME).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("tasks", "0001_initial"),
        ("users", "0001_initial"),
        ("auth", "0001_initial"),
        ("contenttypes", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_group, remove_default_group),
    ]
