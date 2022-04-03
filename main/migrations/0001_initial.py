# Generated by Django 3.2.2 on 2022-02-12 09:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=150)),
                ('image', models.ImageField(default='', upload_to='category')),
                ('description', models.TextField(max_length=250)),
                ('status', models.BooleanField(default=False, help_text='0=default, 1=Hidden')),
            ],
        ),
        migrations.CreateModel(
            name='FeatureProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=50)),
                ('desc', models.CharField(max_length=300)),
                ('price', models.IntegerField()),
                ('image', models.ImageField(default='', upload_to='product')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(max_length=150)),
                ('name', models.CharField(max_length=150)),
                ('product_image', models.ImageField(default='', upload_to='cat_product')),
                ('small_description', models.CharField(default='', max_length=250)),
                ('quantity', models.IntegerField()),
                ('description', models.TextField(max_length=500)),
                ('status', models.BooleanField(default=False, help_text='0=default, 1=Hidden')),
                ('price', models.IntegerField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.category')),
            ],
        ),
    ]
