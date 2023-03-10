# Generated by Django 2.0.4 on 2018-12-02 01:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app1', '0005_auto_20181130_2028'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trade',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oid', models.CharField(max_length=100)),
                ('order_time', models.DateTimeField(auto_now_add=True)),
                ('users', models.CharField(max_length=50)),
                ('product_name', models.CharField(max_length=50)),
                ('amount', models.IntegerField()),
                ('price', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=50)),
                ('message', models.CharField(max_length=100)),
                ('total_price', models.CharField(max_length=50)),
                ('status', models.IntegerField()),
                ('show', models.IntegerField()),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='app1.Product')),
            ],
        ),
    ]
