from django.shortcuts import render, redirect

def home(request):
    if request.user.is_authenticated:
        return redirect('gallery:lista_obras')
    return render(request, 'home.html')  # Cambiado de home.html a index.html

def politicas_privacidad(request):
    return render(request, 'politicas-privacidad.html')

def terminos_condiciones(request):
    return render(request, 'terminos-condiciones.html')

def contacto(request):
    return render(request, 'contacto.html')

# Vistas de error
def error_400(request, exception):
    return render(request, '400.html', status=400)

def error_403(request, exception):
    return render(request, '403.html', status=403)

def error_404(request, exception):
    return render(request, '404.html', status=404)

def error_500(request):
    return render(request, '500.html', status=500)

