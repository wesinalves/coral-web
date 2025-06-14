# Generated by Django 5.1.2 on 2025-06-01 18:27

import django.contrib.auth.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=100)),
                ('date', models.DateField()),
                ('location', models.CharField(max_length=100)),
                ('updated_at', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('phone', models.CharField(max_length=20)),
                ('birthday', models.DateField()),
                ('address', models.CharField(max_length=100)),
                ('suit', models.CharField(choices=[('ALTO', 'Alto'), ('SOPRANO', 'Soprano'), ('BARITONO', 'Baritono'), ('BAIXO', 'Baixo'), ('TENOR', 'Tenor')], default='TENOR', max_length=20)),
                ('terms_agreed', models.BooleanField(default=False)),
                ('created_at', models.DateField()),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Music',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('author', models.CharField(max_length=30)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='covers/')),
                ('year', models.DateField()),
                ('letter', models.TextField()),
                ('created_at', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('url', models.CharField(blank=True, max_length=150, null=True)),
                ('created_at', models.DateField()),
                ('type', models.CharField(choices=[('partitura', 'Partitura'), ('audio', 'Audio'), ('letra', 'Letra'), ('cifra', 'Cifra')], default='TENOR', max_length=20)),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.music')),
            ],
        ),
        migrations.CreateModel(
            name='MusicMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateField()),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.member')),
                ('music', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='webapp.music')),
            ],
            options={
                'unique_together': {('member', 'music')},
            },
        ),
        migrations.AddField(
            model_name='music',
            name='members',
            field=models.ManyToManyField(through='webapp.MusicMember', to='webapp.member'),
        ),
        migrations.CreateModel(
            name='Notice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=100)),
                ('created_at', models.DateField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
