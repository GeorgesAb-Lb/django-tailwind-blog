# Generated by Django 4.1.4 on 2023-11-05 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_blog_thumbnail_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=250)),
                ('phone', models.TextField(max_length=150)),
                ('message', models.TextField(max_length=500)),
            ],
        ),
    ]
