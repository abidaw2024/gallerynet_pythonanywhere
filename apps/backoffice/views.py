from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.gallery.models import Comision
from apps.users.models import Usuario
from apps.sales.models import Order, Encargo
from apps.users.decorators import admin_required

def is_admin(user):
    return user.is_staff

@login_required
@admin_required
def admin_dashboard(request):
    
    # TOTAL OBRAS Y USUARIOS
    total_obras = Comision.objects.count()
    total_usuarios = Usuario.objects.count()
    
    # VENTAS TOTALES (encargos aceptados)
    ventas_totales = Encargo.objects.filter(estado='Aceptado').count()
    
    # INGRESOS TOTALES
    encargos_aceptados = Encargo.objects.filter(estado='Aceptado')
    ingresos_mes = 0
    for encargo in encargos_aceptados:
        if encargo.plan == 'basico':
            ingresos_mes += encargo.obra.precio_basico
        elif encargo.plan == 'estandar':
            ingresos_mes += encargo.obra.precio_estandar
        elif encargo.plan == 'premium':
            ingresos_mes += encargo.obra.precio_premium

    #Obtengo el resultado de todo para usarlo en el html
    context = {
        'total_obras': total_obras,
        'total_usuarios': total_usuarios,
        'ventas_totales': ventas_totales,
        'ingresos_mes': round(ingresos_mes, 2),
    }
    
    return render(request, 'backoffice/dashboard.html', context)