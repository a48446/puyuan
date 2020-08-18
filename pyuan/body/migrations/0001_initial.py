# Generated by Django 2.1 on 2020-08-15 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Blood_pressure',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=100)),
                ('systolic', models.FloatField(default=0, max_length=3, null=True)),
                ('diastolic', models.FloatField(default=0, max_length=3, null=True)),
                ('pulse', models.CharField(default=0, max_length=3, null=True)),
                ('recorded_at', models.DateTimeField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Blood_sugar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=100)),
                ('sugar', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=5, null=True)),
                ('timeperiod', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=5, null=True)),
                ('recorded_at', models.DateTimeField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Diary_diet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=100)),
                ('description', models.CharField(blank=True, default=0, max_length=5, null=True)),
                ('meal', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=5, null=True)),
                ('tag', models.CharField(blank=True, max_length=100)),
                ('image', models.ImageField(blank=True, upload_to='diet/diet_%Y-%m-%d_%H:%M:%S')),
                ('image_count', models.IntegerField(blank=True)),
                ('lat', models.FloatField(blank=True, max_length=100)),
                ('lng', models.FloatField(blank=True, max_length=100)),
                ('recorded_at', models.DateTimeField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserCare',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=100)),
                ('member_id', models.CharField(blank=True, max_length=100)),
                ('reply_id', models.IntegerField(blank=True, null=True)),
                ('message', models.CharField(blank=True, max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(blank=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Weight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uid', models.CharField(blank=True, max_length=100)),
                ('weight', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=5, null=True)),
                ('body_fat', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=5, null=True)),
                ('bmi', models.DecimalField(blank=True, decimal_places=0, default=0, max_digits=5, null=True)),
                ('recorded_at', models.DateTimeField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
    ]
