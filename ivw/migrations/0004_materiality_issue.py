# Generated by Django 5.1.6 on 2025-02-21 14:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ivw', '0003_sdg_remove_user_status_user_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='Materiality_Issue',
            fields=[
                ('materiality_issue_id', models.AutoField(primary_key=True, serialize=False)),
                ('materiality_issue_group', models.CharField(max_length=200)),
                ('theme', models.CharField(max_length=200)),
                ('criterion', models.CharField(max_length=200)),
                ('description', models.TextField()),
            ],
        ),
    ]
