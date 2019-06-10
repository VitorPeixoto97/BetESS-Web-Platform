# Generated by Django 2.2 on 2019-06-05 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bet',
            name='match',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='bet',
            name='user',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='bet',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.Bet'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='user',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]