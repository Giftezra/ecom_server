# Generated by Django 4.2.5 on 2023-09-14 00:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('delivery', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='deliverystatus',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.orders'),
        ),
        migrations.AddField(
            model_name='deliveryperson',
            name='payment_preference',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='main.paymentpreference'),
        ),
        migrations.AddField(
            model_name='deliveryperson',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='deliverymethod',
            name='delivery_personel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.deliveryperson'),
        ),
        migrations.AddField(
            model_name='delivereditems',
            name='delivery_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='delivery.deliveryperson'),
        ),
        migrations.AddField(
            model_name='delivereditems',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.orders'),
        ),
    ]
