# Generated by Django 5.0.7 on 2024-07-17 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coffeeapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('login_id', models.IntegerField()),
                ('name', models.CharField(max_length=100)),
                ('contact', models.IntegerField()),
                ('location', models.CharField(max_length=100)),
            ],
        ),
    ]
