# Generated by Django 3.2.2 on 2022-02-20 02:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='new_arrival',
            field=models.BooleanField(default=False, help_text='0=default, 1=NEW'),
        ),
        migrations.AddField(
            model_name='product',
            name='trending',
            field=models.BooleanField(default=False, help_text='0=default, 1=Trending'),
        ),
    ]
