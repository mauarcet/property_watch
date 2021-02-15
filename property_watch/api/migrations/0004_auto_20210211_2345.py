# Generated by Django 3.1.6 on 2021-02-11 23:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20210211_2120'),
    ]

    operations = [
        migrations.AddField(
            model_name='property',
            name='price',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='property',
            name='size',
            field=models.CharField(max_length=100),
        ),
    ]
