# Generated by Django 3.2.3 on 2021-05-31 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20210531_1822'),
    ]

    operations = [
        migrations.CreateModel(
            name='Toppings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('amount', models.FloatField(default=0.0)),
                ('image', models.FileField(blank=True, null=True, upload_to='')),
                ('food_category', models.PositiveSmallIntegerField(choices=[(1, 'Veg'), (2, 'Non Veg')], default=1)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
