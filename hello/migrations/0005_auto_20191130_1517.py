# Generated by Django 2.2.6 on 2019-11-30 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0004_delete_greeting'),
    ]

    operations = [
        migrations.CreateModel(
            name='Similaridade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('percentual', models.FloatField()),
                ('tipo', models.IntegerField(choices=[(1, 'Levenshtein'), (2, 'Jaccard'), (3, 'Cosine')])),
                ('similar', models.IntegerField()),
            ],
        ),
        migrations.AddField(
            model_name='noticia',
            name='similares',
            field=models.ManyToManyField(to='hello.Similaridade'),
        ),
    ]