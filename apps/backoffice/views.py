from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Count, Sum
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
    
    # Estadísticas de ventas del mes
    ventas_mes = Order.objects.filter(
        created_at__gte=thirty_days_ago,
        status='completed'
    ).count()
    
    ingresos_mes = Order.objects.filter(
        created_at__gte=thirty_days_ago,
        status='completed'
    ).aggregate(total=Sum('total'))['total'] or 0

    # Distribución de usuarios
    vendedores = Usuario.objects.filter(es_vendedor=True).count()
    compradores = Usuario.objects.filter(es_comprador=True).count()

    # Últimas ventas
    ultimas_ventas = Order.objects.select_related('user').order_by('-created_at')[:10]

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
        'ventas_mes': ventas_mes,
        'ingresos_mes': round(ingresos_mes, 2),
        'vendedores': vendedores,
        'compradores': compradores,
        'ultimas_ventas': ultimas_ventas,
        'ventas_por_mes': ventas_por_mes,
    }
    
    return render(request, 'backoffice/dashboard.html', context)