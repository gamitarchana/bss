# Generated by Django 3.0 on 2020-01-17 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdditionalServiceCharge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('duration_in_days', models.PositiveSmallIntegerField()),
                ('additionl_charges', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='BabysitterRecommendation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'available'), (2, 'recommended'), (3, 'active'), (4, 'rejected')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='BasicServicePackage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('hours_per_day', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('duration_in_days', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('charges', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Child',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=50)),
                ('last_name', models.CharField(max_length=50)),
                ('date_of_birth', models.DateField()),
                ('gender', models.PositiveSmallIntegerField(choices=[(1, 'female'), (2, 'male')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('description', models.CharField(blank=True, max_length=500, null=True)),
                ('icon', models.ImageField(blank=True, null=True, upload_to='service_icons')),
            ],
        ),
        migrations.CreateModel(
            name='Shift',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.PositiveSmallIntegerField(choices=[(1, 'Day'), (2, 'Night')], default=1)),
                ('hours_per_day', models.PositiveSmallIntegerField(choices=[(1, 8), (2, 10), (3, 12)], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='ShiftTimeSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('shift', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='time_slots', to='bssservices.Shift')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceRequest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'new'), (2, 'new profile'), (3, 'profile accepted'), (4, 'profile rejected'), (5, 'meeting scheduled'), (6, 'meeting reschedule request'), (7, 'meeting accepted'), (8, 'meeting done'), (9, 'wallet recharge pending'), (10, 'wallet recharged'), (11, 'trail'), (12, 'accepted'), (13, 'rejected'), (14, 'payment due')], default=1)),
                ('additional_service_charges', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='bssservices.AdditionalServiceCharge')),
            ],
        ),
    ]
