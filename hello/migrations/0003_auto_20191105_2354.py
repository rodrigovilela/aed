# Generated by Django 2.2.6 on 2019-11-06 02:54

from django.db import migrations, models
import hello.models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0002_auto_20191104_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trecho',
            name='tipo',
            field=models.IntegerField(choices=[(1, 'TEXTO_NORMAL'), (2, 'HASH_12'), (3, 'OUTRO')], default=hello.models.TipoTrecho(1)),
        ),
        migrations.AlterField(
            model_name='trecho',
            name='valor',
            field=models.TextField(),
        ),
    ]
