import os
import django
from datetime import date, timedelta
from decimal import Decimal

# 👇 Debe coincidir EXACTO con tu proyecto (carpeta donde está settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'INVENTARIO_TITULACION.settings')
django.setup()

from inventario.models import Categoria, Producto

def crear_categorias():
    print("\n📁 Creando categorías (get_or_create)...")
    nombres = ["MEDICAMENTOS", "VACUNAS", "ALIMENTOS", "HIGIENE Y LIMPIEZA", "INSUMOS MÉDICOS"]
    creadas = {}
    for nombre in nombres:
        cat, _ = Categoria.objects.get_or_create(nombre=nombre)
        creadas[nombre] = cat
        print(f"  ✅ {cat.nombre}")
    return creadas

def crear_productos(categorias):
    print("\n📦 Creando productos (get_or_create por código)...")
    hoy = date.today()
    productos_data = [
        {
            'nombre': 'Amoxicilina 500mg',
            'codigo': 'MED-001',
            'categoria': 'MEDICAMENTOS',
            'descripcion': 'Antibiótico de amplio espectro',
            'precio_costo': Decimal('8.50'),
            'precio_venta': Decimal('15.00'),
            'stock': 40,
            'stock_minimo': 20,
            'fecha_vencimiento': hoy + timedelta(days=365*2),
        },
        {
            'nombre': 'Vacuna Antirrábica 10ml',
            'codigo': 'VAC-001',
            'categoria': 'VACUNAS',
            'descripcion': 'Dosis múltiples, uso veterinario',
            'precio_costo': Decimal('22.00'),
            'precio_venta': Decimal('35.00'),
            'stock': 15,
            'stock_minimo': 8,
            'fecha_vencimiento': hoy + timedelta(days=365),
        },
        {
            'nombre': 'Alimento Canino Adulto 15kg',
            'codigo': 'ALI-001',
            'categoria': 'ALIMENTOS',
            'descripcion': 'Balanceado premium',
            'precio_costo': Decimal('28.00'),
            'precio_venta': Decimal('42.00'),
            'stock': 18,
            'stock_minimo': 6,
            'fecha_vencimiento': None,
        },
        {
            'nombre': 'Desinfectante Quirúrgico 5L',
            'codigo': 'HIG-001',
            'categoria': 'HIGIENE Y LIMPIEZA',
            'descripcion': 'Uso hospitalario',
            'precio_costo': Decimal('18.00'),
            'precio_venta': Decimal('28.00'),
            'stock': 12,
            'stock_minimo': 6,
            'fecha_vencimiento': hoy + timedelta(days=540),
        },
        {
            'nombre': 'Guantes Nitrilo Talla M (caja x100)',
            'codigo': 'INS-001',
            'categoria': 'INSUMOS MÉDICOS',
            'descripcion': 'Descartables',
            'precio_costo': Decimal('6.50'),
            'precio_venta': Decimal('10.00'),
            'stock': 25,
            'stock_minimo': 10,
            'fecha_vencimiento': None,
        },
    ]

    creados = 0
    for p in productos_data:
        cat = categorias.get(p['categoria'])
        if not cat:
            print(f"  ⚠️ Categoría no encontrada: {p['categoria']} (producto {p['codigo']})")
            continue

        defaults = {
            'nombre': p['nombre'],
            'descripcion': p['descripcion'],
            'precio_costo': p['precio_costo'],
            'precio_venta': p['precio_venta'],
            'stock': p['stock'],
            'stock_minimo': p['stock_minimo'],
            'fecha_vencimiento': p['fecha_vencimiento'],
            'categoria': cat,
        }

        producto, created = Producto.objects.get_or_create(
            codigo=p['codigo'],
            defaults=defaults
        )
        if created:
            creados += 1
            print(f"  ✅ {producto.codigo} - {producto.nombre}")
        else:
            print(f"  ℹ️ Ya existía: {producto.codigo} - {producto.nombre}")

    print(f"\n✅ Total creados: {creados}")

def main():
    print("🚀 Poblando base de datos...")
    categorias = crear_categorias()
    crear_productos(categorias)
    print("\n🎉 Listo.")

if __name__ == '__main__':
    main()
