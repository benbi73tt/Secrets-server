# Generated by Django 4.1.7 on 2023-12-18 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ballroom', '0002_user_sur_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('date', models.CharField(max_length=200)),
            ],
        ),
    ]
