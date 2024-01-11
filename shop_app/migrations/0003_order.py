# Generated by Django 5.0 on 2024-01-10 07:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop_app', '0002_product_video'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name="Ім'я отримувача")),
                ('surname', models.CharField(max_length=255, verbose_name='Прізвище отримувача')),
                ('patronymic', models.CharField(max_length=255, verbose_name='Побатькові отримувача')),
                ('phone', models.CharField(max_length=255, verbose_name='Телефон отримувача')),
                ('selectedcity', models.CharField(max_length=255, verbose_name='Місто отримувача')),
                ('selectedwarehouse', models.CharField(max_length=255, verbose_name='Пункт отримання')),
                ('products', models.TextField(verbose_name='Замовлені товари')),
                ('status', models.CharField(choices=[(1, 'Виконується'), (2, 'Виконано')], max_length=255, verbose_name='Статус замовлення')),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop_app.cart', verbose_name='Корзина')),
            ],
            options={
                'verbose_name': 'Замовлення',
                'verbose_name_plural': 'Замовлення',
            },
        ),
    ]