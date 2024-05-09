# Generated by Django 5.0.4 on 2024-05-09 10:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('email', models.EmailField(help_text='Введите email', max_length=64, unique=True, verbose_name='email')),
                ('first_name', models.CharField(blank=True, help_text='Введите имя', max_length=64, null=True, verbose_name='имя пользователя')),
                ('last_name', models.CharField(blank=True, help_text='Введите фамилию', max_length=64, null=True, verbose_name='фамилия пользователя')),
                ('is_staff', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'пользователь',
                'verbose_name_plural': 'пользователи',
                'db_table': 'users',
                'ordering': ['email'],
            },
        ),
    ]
