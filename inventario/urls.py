from django.urls import path, include
from django.shortcuts import render, redirect
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .views import (CategoriaViewSet, ProductoViewSet,
                    MovimientoViewSet, ProveedorViewSet,
                    productos_lista, inicio)

router = DefaultRouter()
router.register(r'categorias', CategoriaViewSet)
router.register(r'productos', ProductoViewSet)
router.register(r'movimientos', MovimientoViewSet)
router.register(r'proveedores', ProveedorViewSet)

@api_view(['GET'])
def api_root(request):
    return Response({
        'mensaje': 'Bienvenido a la API de Inventario',
        'endpoints': {
            'categorias': '/api/categorias/',
            'productos': '/api/productos/',
            'movimientos': '/api/movimientos/',
            'proveedores': '/api/proveedores/',
        }
    })

urlpatterns = [
    # Raíz
    path('', inicio, name='inicio'),
    
    # Templates HTML
    path('productos/', productos_lista, name='productos-lista'),
    
    # API REST
    path('api/', api_root, name='api-root'),
    path('api/', include(router.urls)),
]