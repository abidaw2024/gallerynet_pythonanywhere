from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Categoria
from .forms import CategoriaForm
from apps.users.decorators import admin_required

#Listar todas las categorías en el panel de administración
@login_required
@admin_required
def admin_categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'backoffice/admin_categoria_list.html', {'categorias': categorias})

#Ver los detalles de una categoría específica
@login_required
@admin_required
def admin_categoria_detail(request, pk):
    try:
        categoria = Categoria.objects.get(pk=pk)
        return render(request, 'backoffice/admin_categoria_detail.html', {'categoria': categoria})
    except Categoria.DoesNotExist:
        messages.error(request, 'La categoría no existe.')
        return redirect('categories:admin_categoria_list')

#Vista para crear una nueva categoría
@login_required
@admin_required
def admin_categoria_create(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría creada exitosamente.')
            return redirect('categories:admin_categoria_list')
    else:
        form = CategoriaForm()
    return render(request, 'backoffice/admin_categoria_update.html', {'form': form})

#Vista para actualizar una categoría
@login_required
@admin_required
def admin_categoria_update(request, pk):
    try:
        categoria = Categoria.objects.get(pk=pk)
        if request.method == 'POST':
            form = CategoriaForm(request.POST, instance=categoria)
            if form.is_valid():
                form.save()
                messages.success(request, 'Categoría actualizada exitosamente.')
                return redirect('categories:admin_categoria_list')
        else:
            form = CategoriaForm(instance=categoria)
        return render(request, 'backoffice/admin_categoria_update.html', {'form': form})
    
    except Categoria.DoesNotExist:
        messages.error(request, 'La categoría no existe.')
        return redirect('categories:admin_categoria_list')

#Vista para eliminar una categoría
@login_required
@admin_required
def admin_categoria_delete(request, pk):
    try:
        categoria = Categoria.objects.get(pk=pk)
        if request.method == 'POST':
            categoria.delete()
            messages.success(request, 'Categoría eliminada exitosamente.')
            return redirect('categories:admin_categoria_list')
        return redirect('categories:admin_categoria_list')
    
    except Categoria.DoesNotExist:
        messages.error(request, 'La categoría no existe.')
        return redirect('categories:admin_categoria_list') 