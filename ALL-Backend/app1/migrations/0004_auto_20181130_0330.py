# Generated by Django 2.0.4 on 2018-11-30 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0003_article1_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article1',
            name='title',
            field=models.CharField(max_length=50),
        ),
    ]
