#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate

# Crear superusuario automáticamente
echo "from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin', 'admin@example.com', 'admin123')" | python manage.py shell

# Cargar datos iniciales de productos
python manage.py shell << END
from productos.models import Producto, Categoria

# Crear categorías si no existen
categorias = ['LIMPIEZA', 'INSUMOS MÉDICOS', 'HIGIENE Y LIMPIEZA', 'ALIMENTOS', 'VACUNAS', 'MEDICAMENTOS']
for cat in categorias:
    Categoria.objects.get_or_create(nombre=cat)

# Crear productos si no existen
productos = [
    {"codigo": "gas-004", "nombre": "gasas", "categoria": "LIMPIEZA", "existencias": 10, "precio": 0.65},
    {"codigo": "PEN-500", "nombre": "Penicilina 500mg", "categoria": "LIMPIEZA", "existencias": 50, "precio": 13.00},
    {"codigo": "NIT-001", "nombre": "Guantes Nitrilo Talla M", "categoria": "INSUMOS MÉDICOS", "existencias": 25, "precio": 10.00},
    {"codigo": "DES-001", "nombre": "Desinfectante Quirúrgico 5L", "categoria": "HIGIENE Y LIMPIEZA", "existencias": 12, "precio": 28.00},
    {"codigo": "ALI-001", "nombre": "Alimento Canino Adulto 15kg", "categoria": "ALIMENTOS", "existencias": 18, "precio": 42.00},
    {"codigo": "VAC-001", "nombre": "Vacuna Antirrábica 10ml", "categoria": "VACUNAS", "existencias": 15, "precio": 35.00},
    {"codigo": "MED-001", "nombre": "Amoxicilina 500mg", "categoria": "MEDICAMENTOS", "existencias": 40, "precio": 15.00}
]

for prod in productos:
    cat = Categoria.objects.get(nombre=prod.pop('categoria'))
    Producto.objects.get_or_create(codigo=prod['codigo'], defaults={**prod, 'categoria': cat})
    
print("Datos cargados exitosamente!")
END