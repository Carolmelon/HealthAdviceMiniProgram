# Generated by Django 2.0.4 on 2018-12-05 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0014_user_telephone'),
    ]

    operations = [
        migrations.AddField(
            model_name='trade',
            name='notify_status',
            field=models.IntegerField(default=1),
        ),
    ]
