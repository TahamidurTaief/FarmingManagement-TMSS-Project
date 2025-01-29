# Generated by Django 5.1.1 on 2024-09-17 12:09

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='donation',
            old_name='amount',
            new_name='donation_amount',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='date',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='description',
        ),
        migrations.RemoveField(
            model_name='donation',
            name='farmer',
        ),
        migrations.AddField(
            model_name='donation',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donation',
            name='donor_email',
            field=models.EmailField(default=django.utils.timezone.now, max_length=254),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donation',
            name='donor_name',
            field=models.CharField(default=django.utils.timezone.now, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donation',
            name='donor_phone',
            field=models.CharField(default=0, max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='donation',
            name='transaction_id',
            field=models.CharField(default=1, max_length=100),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='FarmerPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='donation',
            name='farmer_post',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, related_name='donations', to='app.farmerpost'),
            preserve_default=False,
        ),
    ]
