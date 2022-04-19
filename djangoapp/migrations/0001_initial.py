# Generated by Django 4.0.4 on 2022-04-19 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('uploader', models.CharField(max_length=20)),
                ('product_desc', models.TextField()),
                ('target', models.IntegerField(default=0)),
                ('fund_now', models.IntegerField(default=0)),
                ('end_day', models.IntegerField(default=0)),
                ('target_day', models.DateTimeField(auto_now=True, null=True)),
                ('one_fund', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
            ],
        ),
    ]
