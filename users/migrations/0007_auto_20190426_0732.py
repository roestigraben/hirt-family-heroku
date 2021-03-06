# Generated by Django 2.0 on 2019-04-26 07:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20190425_2058'),
    ]

    operations = [
        migrations.CreateModel(
            name='XtraInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=100)),
                ('text', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Extra Information',
            },
        ),
        migrations.AddField(
            model_name='xtrainfo',
            name='parent',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.Person'),
        ),
    ]
