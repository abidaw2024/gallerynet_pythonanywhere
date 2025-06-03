import imaplib
import email
from email.header import decode_header
from django.conf import settings
from .services import EmailService

#clase para recibir correos de gmail
class ReceptorEmail:
    def __init__(self):
        self.imap_server = settings.EMAIL_HOST
        self.email = settings.EMAIL_HOST_USER
        self.password = settings.EMAIL_HOST_PASSWORD
        self.imap = None

    def conectar(self):
        """Establece conexión con el servidor IMAP"""
        try:
            self.imap = imaplib.IMAP4_SSL(self.imap_server)
            self.imap.login(self.email, self.password)
            return True
        except Exception as e:
            print(f"Error al conectar: {str(e)}")
            return False

    def desconectar(self):
        """Cierra la conexión con el servidor IMAP"""
        if self.imap:
            try:
                self.imap.close()
                self.imap.logout()
            except:
                pass

    def obtener_contenido_email(self, msg):
        """Extrae el contenido de un email"""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    return part.get_payload(decode=True).decode()
        return msg.get_payload(decode=True).decode()

    def extraer_info_correo(self, msg):
        """Extrae la información básica de un correo"""
        asunto = ""
        for part in decode_header(msg["subject"]):
            if isinstance(part[0], bytes):
                asunto += part[0].decode(part[1] or 'utf-8')
            else:
                asunto += part[0]

        remitente = ""
        for part in decode_header(msg["from"]):
            if isinstance(part[0], bytes):
                remitente += part[0].decode(part[1] or 'utf-8')
            else:
                remitente += part[0]

        return {
            'subject': asunto,
            'from_email': remitente,
            'body': self.obtener_contenido_email(msg)
        }

    def procesar_un_correo(self, num):
        """Procesa un correo individual"""
        try:
            _, msg_data = self.imap.fetch(num, '(RFC822)')
            email_body = msg_data[0][1]
            msg = email.message_from_bytes(email_body)
            
            # Extraer información del correo
            info = self.extraer_info_correo(msg)
            
            # Procesar la respuesta
            EmailService.procesar_respuesta_email(info)
            
            # Marcar como leído
            self.imap.store(num, '+FLAGS', '\\Seen')
            return True
        except Exception as e:
            print(f"Error al procesar correo {num}: {str(e)}")
            return False

    def procesar_correos(self):
        """Procesa todos los correos no leídos"""
        if not self.conectar():
            return False

        try:
            # Seleccionar la bandeja de entrada
            self.imap.select('INBOX')
            
            # Buscar correos no leídos
            _, mensajes = self.imap.search(None, 'UNSEEN')
            
            # Procesar cada correo
            for num in mensajes[0].split():
                self.procesar_un_correo(num)
                
            return True
        except Exception as e:
            print(f"Error al procesar correos: {str(e)}")
            return False
        finally:
            self.desconectar()

def verificar_correos():
    """Función para verificar y procesar correos entrantes"""
    receptor = ReceptorEmail()
    return receptor.procesar_correos()