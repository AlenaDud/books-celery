# Generated by Django 5.0.7 on 2024-07-24 19:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='book',
            options={'ordering': ['-rating'], 'verbose_name': 'book', 'verbose_name_plural': 'books'},
        ),
    ]