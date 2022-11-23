# Generated by Django 4.1.1 on 2022-11-23 11:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0024_alter_customeraddress_address_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customeraddress',
            name='address',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='area',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.area'),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='city',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.city'),
        ),
        migrations.AlterField(
            model_name='customeraddress',
            name='province',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='store.province'),
        ),
    ]