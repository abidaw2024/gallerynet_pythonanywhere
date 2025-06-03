from django.core.management.base import BaseCommand
from apps.mensajes.email_receiver import verificar_correos

#comando de Django para verificar y procesar correos entrantes
class Command(BaseCommand):
    help = 'Verifica y procesa correos entrantes'

    def handle(self, *args, **options):
        self.stdout.write('Verificando correos entrantes...')
        verificar_correos()
        self.stdout.write(self.style.SUCCESS('Verificación de correos completada')) 