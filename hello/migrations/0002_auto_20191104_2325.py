# Generated by Django 2.2.6 on 2019-11-05 02:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trecho',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=255)),
                ('tipo', models.IntegerField(choices=[(1, 'Texto normal'), (2, 'Hash de tamanho 12'), (3, '...')])),
            ],
        ),
        migrations.AlterField(
            model_name='greeting',
            name='when',
            field=models.DateTimeField(auto_now_add=True, verbose_name='date created'),
        ),
        migrations.CreateModel(
            name='Noticia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=255)),
                ('texto', models.TextField()),
                ('publicacao', models.DateField()),
                ('veiculo', models.CharField(max_length=255)),
                ('trechos', models.ManyToManyField(to='hello.Trecho')),
            ],
        ),
    ]
