# Generated by Django 5.0.4 on 2024-04-21 10:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('TaskAppWeb', '0007_remove_task_archived_remove_task_assigned_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Task',
            new_name='TaskYougile',
        ),
    ]