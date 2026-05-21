from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('prestamos', '0001_initial'),
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('APROBACION', 'Aprobación de Préstamo'), ('VENCIMIENTO', 'Recordatorio de Vencimiento'), ('DEVOLUCION', 'Confirmación de Devolución'), ('RETRASO', 'Notificación de Retraso')], default='VENCIMIENTO', max_length=20)),
                ('estado', models.CharField(choices=[('PENDIENTE', 'Pendiente'), ('ENVIADA', 'Enviada'), ('FALLIDA', 'Fallida'), ('CANCELADA', 'Cancelada')], default='PENDIENTE', max_length=20)),
                ('asunto', models.CharField(max_length=200)),
                ('mensaje', models.TextField()),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_envio', models.DateTimeField(blank=True, null=True)),
                ('intentos', models.IntegerField(default=0)),
                ('error', models.TextField(blank=True)),
                ('prestamo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones', to='prestamos.prestamo')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='notificaciones_recibidas', to='auth.user')),
            ],
            options={
                'verbose_name': 'notificación',
                'verbose_name_plural': 'notificaciones',
                'ordering': ['-fecha_creacion'],
            },
        ),
        migrations.AddIndex(
            model_name='notificacion',
            index=models.Index(fields=['estado', 'tipo'], name='notificacio_estado_tipo_idx'),
        ),
        migrations.AddIndex(
            model_name='notificacion',
            index=models.Index(fields=['usuario', 'fecha_creacion'], name='notificacio_usuario_fecha_idx'),
        ),
    ]
