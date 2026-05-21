# Generated migration

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prestamos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='prestamo',
            name='notificacion_vencimiento_enviada',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='prestamo',
            name='fecha_notificacion_enviada',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
