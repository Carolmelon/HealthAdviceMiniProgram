# Generated by Django 2.0.4 on 2018-12-05 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0016_auto_20181205_2116'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='pay_time',
            field=models.DateTimeField(null=True),
        ),
    ]
