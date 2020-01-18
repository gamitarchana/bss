# Generated by Django 3.0 on 2020-01-17 17:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('bsscore', '0001_initial'),
        ('bssservices', '0001_initial'),
        ('bssuser', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicerequest',
            name='babysitter_recommendations',
            field=models.ManyToManyField(through='bssservices.BabysitterRecommendation', to='bssuser.Babysitter'),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='basic_service_package',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='bssservices.BasicServicePackage'),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='client',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='bssuser.Client'),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='location',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='bsscore.ServiceArea'),
        ),
        migrations.AddField(
            model_name='servicerequest',
            name='shift_time_slot',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='service_requests', to='bssservices.ShiftTimeSlot'),
        ),
        migrations.AddField(
            model_name='child',
            name='service_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='children', to='bssservices.ServiceRequest'),
        ),
        migrations.AddField(
            model_name='basicservicepackage',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='basic_service_package', to='bssservices.Service'),
        ),
        migrations.AddField(
            model_name='babysitterrecommendation',
            name='babysitter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to='bssuser.Babysitter'),
        ),
        migrations.AddField(
            model_name='babysitterrecommendation',
            name='service_request',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recommendations', to='bssservices.ServiceRequest'),
        ),
        migrations.AddField(
            model_name='additionalservicecharge',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='extra_service_package', to='bssservices.Service'),
        ),
    ]
