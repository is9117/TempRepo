# Generated by Django 3.0.14 on 2023-05-17 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(blank=True, max_length=16, null=True)),
                ('price', models.IntegerField(default=0)),
                ('cost', models.IntegerField(default=0)),
                ('name', models.CharField(blank=True, max_length=128, null=True)),
                ('description', models.CharField(blank=True, max_length=1024, null=True)),
                ('barcode', models.CharField(blank=True, max_length=128, null=True)),
                ('expiration_date', models.DateField(null=True)),
                ('size', models.CharField(choices=[('S', 'small'), ('L', 'large')], max_length=1)),
            ],
            options={
                'ordering': ('-id',),
            },
        ),
    ]
