from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import models
from .models import Categoria, Producto, Movimiento, Proveedor
from .serializers import (CategoriaSerializer, ProductoSerializer, 
                          MovimientoSerializer, ProveedorSerializer)

class CategoriaViewSet(viewsets.ModelViewSet):
    queryset = Categoria.objects.all()
    serializer_class = CategoriaSerializer

class ProductoViewSet(viewsets.ModelViewSet):
    queryset = Producto.objects.all()
    serializer_class = ProductoSerializer
    
    @action(detail=False, methods=['get'])
    def stock_bajo(self, request):
        productos = Producto.objects.filter(stock__lte=models.F('stock_minimo'))
        serializer = self.get_serializer(productos, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def registrar_movimiento(self, request, pk=None):
        producto = self.get_object()
        tipo = request.data.get('tipo')
        cantidad = int(request.data.get('cantidad', 0))
        
        if tipo == 'entrada':
            producto.stock += cantidad
        elif tipo == 'salida':
            if producto.stock < cantidad:
                return Response({'error': 'Stock insuficiente'}, 
                              status=status.HTTP_400_BAD_REQUEST)
            producto.stock -= cantidad
        
        producto.save()
        
        Movimiento.objects.create(
            producto=producto,
            tipo=tipo,
            cantidad=cantidad,
            motivo=request.data.get('motivo', ''),
            usuario=request.user.username or 'admin'
        )
        
        return Response({'stock': producto.stock})

class MovimientoViewSet(viewsets.ModelViewSet):
    queryset = Movimiento.objects.all()
    serializer_class = MovimientoSerializer

class ProveedorViewSet(viewsets.ModelViewSet):
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

# ========== VISTAS PARA TEMPLATES HTML ==========
from django.views.generic import ListView, DetailView
from datetime import datetime, timedelta

def productos_lista(request):
    from datetime import datetime, timedelta
    
    # Obtener todos los productos
    productos = Producto.objects.select_related('categoria').all()
    
    # Filtros de búsqueda
    busqueda = request.GET.get('busqueda', '')
    categoria_id = request.GET.get('categoria', '')
    
    if busqueda:
        productos = productos.filter(
            models.Q(nombre__icontains=busqueda) | 
            models.Q(codigo__icontains=busqueda)
        )
    
    if categoria_id:
        productos = productos.filter(categoria_id=categoria_id)
    
    # Calcular estadísticas
    total_productos = productos.count()
    stock_bajo = productos.filter(stock__lte=models.F('stock_minimo')).count()
    
    # Productos próximos a vencer (30 días)
    fecha_limite = datetime.now().date() + timedelta(days=30)
    proximamente_vencen = productos.filter(
        fecha_vencimiento__isnull=False,
        fecha_vencimiento__lte=fecha_limite,
        fecha_vencimiento__gte=datetime.now().date()
    ).count()
    
    # Obtener todas las categorías para el filtro
    categorias = Categoria.objects.all()
    
    context = {
        'productos': productos,
        'total_productos': total_productos,
        'stock_bajo': stock_bajo,
        'proximamente_vencen': proximamente_vencen,
        'categorias': categorias,
        'categoria_seleccionada': int(categoria_id) if categoria_id else None,
        'dias_limite': fecha_limite,
    }
    
    return render(request, 'inventario/productos_lista.html', context)

def inicio(request):
    return render(request, 'inventario/inicio.html')