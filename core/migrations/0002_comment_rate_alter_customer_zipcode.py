# Generated by Django 4.0.4 on 2022-12-13 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='rate',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='customer',
            name='zipcode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]