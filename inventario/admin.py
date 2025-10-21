from django.contrib import admin
from .models import Categoria, Producto, Movimiento, Proveedor

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'descripcion']
    search_fields = ['nombre']

@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'stock', 'precio_venta', 'stock_bajo']
    search_fields = ['nombre', 'codigo']
    list_filter = ['categoria', 'activo']

@admin.register(Movimiento)
class MovimientoAdmin(admin.ModelAdmin):
    list_display = ['producto', 'tipo', 'cantidad', 'fecha', 'usuario']
    search_fields = ['producto__nombre']
    list_filter = ['tipo', 'fecha']

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'email', 'telefono']
    search_fields = ['nombre', 'email']
