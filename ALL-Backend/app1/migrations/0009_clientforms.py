# Generated by Django 2.0.4 on 2018-12-03 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0008_imgname'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClientForms',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('types', models.CharField(max_length=50)),
                ('have_pic', models.BooleanField(default=False)),
                ('pics_names', models.TextField()),
                ('other_fields', models.TextField()),
            ],
        ),
    ]