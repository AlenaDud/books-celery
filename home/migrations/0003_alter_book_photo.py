# Generated by Django 5.0.7 on 2024-07-25 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_book_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='book_photos/'),
        ),
    ]
