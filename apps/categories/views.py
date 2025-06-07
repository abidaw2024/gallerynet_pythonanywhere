from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Categoria
from .forms import CategoriaForm
from apps.users.decorators import admin_required

@login_required
@admin_required
def admin_categoria_list(request):
    categorias = Categoria.objects.all()
    return render(request, 'backoffice/admin_categoria_list.html', {'categorias': categorias})

@login_required
@admin_required
def admin_categoria_detail(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    return render(request, 'backoffice/admin_categoria_detail.html', {'categoria': categoria})

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

@login_required
@admin_required
def admin_categoria_update(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoría actualizada exitosamente.')
            return redirect('categories:admin_categoria_list')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'backoffice/admin_categoria_update.html', {'form': form})

@login_required
@admin_required
def admin_categoria_delete(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)
    if request.method == 'POST':
        categoria.delete()
        messages.success(request, 'Categoría eliminada exitosamente.')
        return redirect('categories:admin_categoria_list')
    return redirect('categories:admin_categoria_list') 