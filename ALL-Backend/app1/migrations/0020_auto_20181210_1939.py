# Generated by Django 2.0.4 on 2018-12-10 19:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0019_clientforms_time'),
    ]

    operations = [
        migrations.CreateModel(
            name='adminUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.AlterField(
            model_name='clientforms',
            name='time',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]