# Generated by Django 3.2 on 2021-05-31 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Accueil', '0007_article_fichier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='titre',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='auteur',
            name='nom',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='conference',
            name='chair',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='conference',
            name='lieu',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='conference',
            name='nom',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='conference',
            name='organisateur',
            field=models.CharField(max_length=1000),
        ),
        migrations.AlterField(
            model_name='motcle',
            name='mot',
            field=models.CharField(max_length=1000),
        ),
    ]
