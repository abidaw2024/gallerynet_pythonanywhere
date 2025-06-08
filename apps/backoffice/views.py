from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum, F
from django.utils import timezone
from datetime import timedelta
from apps.gallery.models import Comision
from apps.users.models import Usuario
from apps.sales.models import Order
from apps.users.decorators import admin_required

def is_admin(user):
    return user.is_staff

@login_required
@admin_required
def admin_dashboard(request):
    # Fecha actual y hace 30 días
    now = timezone.now()
    thirty_days_ago = now - timedelta(days=30)

    # Estadísticas básicas
    total_obras = Comision.objects.count()
    total_usuarios = Usuario.objects.count()
    
    # Ventas totales = encargos aceptados
    ventas_totales = Order.objects.filter(estado='Aceptado').count()
    
    # Ingresos del mes = suma de precios de encargos aceptados
    ingresos_mes = Order.objects.filter(estado='Aceptado').aggregate(
        total=Sum(F('obra__precio_' + F('plan')))
    )['total'] or 0

    # Distribución de usuarios
    vendedores = Usuario.objects.filter(es_vendedor=True).count()
    compradores = Usuario.objects.filter(es_comprador=True).count()

    # Datos para el gráfico de ventas mensuales
    ventas_por_mes = []
    for i in range(6):
        fecha = now - timedelta(days=30*i)
        ventas = Order.objects.filter(
            created_at__year=fecha.year,
            created_at__month=fecha.month,
            status='completed'
        ).count()
        ventas_por_mes.append(ventas)

    context = {
        'total_obras': total_obras,
        'total_usuarios': total_usuarios,
        'ventas_totales': ventas_totales,
        'ingresos_mes': round(ingresos_mes, 2),
        'vendedores': vendedores,
        'compradores': compradores,
        'ventas_por_mes': ventas_por_mes,
    }
    
    return render(request, 'backoffice/dashboard.html', context)