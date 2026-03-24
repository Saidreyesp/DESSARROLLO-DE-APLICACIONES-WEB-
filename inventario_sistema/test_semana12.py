"""
Tests para validar la implementación de Semana 12

Este script prueba todas las funcionalidades de persistencia de datos
incluyendo TXT, JSON, CSV y SQLite.
"""

import os
import sys
import json
import csv
from datetime import datetime

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from inventario import GestorInventario, Producto
from inventario.persistencia import read_txt, read_json, read_csv


class TestSemana12:
    """Clase para ejecutar tests de Semana 12."""
    
    def __init__(self):
        """Inicializa el contexto de test."""
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        self.tests_pasados = 0
        self.tests_fallidos = 0
    
    def limpiar_base_datos(self):
        """Limpia la base de datos y archivos de test."""
        db.drop_all()
        db.create_all()
        
        # Limpiar archivos de datos
        data_dir = 'inventario/data'
        for archivo in ['datos.txt', 'datos.json', 'datos.csv']:
            filepath = os.path.join(data_dir, archivo)
            if os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    if archivo == 'datos.json':
                        f.write('[]')
                    elif archivo == 'datos.csv':
                        f.write('nombre,precio,cantidad\n')
    
    def test_crear_producto(self):
        """Test: Crear un producto."""
        print("\n[TEST 1] Crear Producto...")
        try:
            producto = GestorInventario.crear_producto(
                nombre='Test Ceviche',
                precio=12.50,
                cantidad=5,
                categoria='Mariscos',
                descripcion='Ceviche de prueba'
            )
            
            assert producto is not None, "Producto no fue creado"
            assert producto.nombre == 'Test Ceviche', "Nombre incorrecto"
            assert producto.precio == 12.50, "Precio incorrecto"
            
            print("✓ PASADO: Producto creado exitosamente")
            self.tests_pasados += 1
            return True
        except Exception as e:
            print(f"✗ FALLIDO: {str(e)}")
            self.tests_fallidos += 1
            return False
    
    def test_obtener_todos(self):
        """Test: Obtener todos los productos."""
        print("\n[TEST 2] Obtener Todos los Productos...")
        try:
            GestorInventario.crear_producto('Test 1', 5.00, 10)
            GestorInventario.crear_producto('Test 2', 8.00, 15)
            
            productos = GestorInventario.obtener_todos()
            assert len(productos) >= 2, "No se obtuvieron todos los productos"
            
            print(f"✓ PASADO: Se obtuvieron {len(productos)} productos")
            self.tests_pasados += 1
            return True
        except Exception as e:
            print(f"✗ FALLIDO: {str(e)}")
            self.tests_fallidos += 1
            return False
    
    def test_obtener_por_id(self):
        """Test: Obtener producto por ID."""
        print("\n[TEST 3] Obtener Producto por ID...")
        try:
            producto = GestorInventario.crear_producto('Test ID', 7.00, 8)
            
            obtenido = GestorInventario.obtener_por_id(producto.id)
            assert obtenido is not None, "Producto no encontrado"
            assert obtenido.nombre == 'Test ID', "Nombre incorrecto"
            
            print("✓ PASADO: Producto obtenido correctamente por ID")
            self.tests_pasados += 1
            return True
        except Exception as e:
            print(f"✗ FALLIDO: {str(e)}")
            self.tests_fallidos += 1
            return False
    
    def test_obtener_por_nombre(self):
        """Test: Obtener producto por nombre."""
        print("\n[TEST 4] Obtener Producto por Nombre...")
        try:
            GestorInventario.crear_producto('Test Nombre Único', 10.00, 5)
            
            obtenido = GestorInventario.obtener_por_nombre('Test Nombre Único')
            assert obtenido is not None, "Producto no encontrado por nombre"
            assert obtenido.nombre == 'Test Nombre Único', "Nombre incorrecto"
            
            print("✓ PASADO: Producto obtening correctamente por nombre")
            self.tests_pasados += 1
            return True
        except Exception as e:
            print(f"✗ FALLIDO: {str(e)}")
            self.tests_fallidos += 1
            return False
    
    def test_actualizar_producto(self):
        """Test: Actualizar producto."""
        print("\n[TEST 5] Actualizar Producto...")
        try:
            producto = GestorInventario.crear_producto('Update Test', 5.00, 10)
            
            GestorInventario.actualizar_producto(
                producto.id,
                precio=6.50,
                cantidad=15
            )
            
            actualizado = GestorInventario.obtener_por_id(producto.id)
            assert actualizado.precio == 6.50, "Precio no actualizado"
            assert actualizado.cantidad == 15, "Cantidad no actualizada"
            
            print("✓ PASADO: Producto actualizado correctamente")
            self.tests_pasados += 1
            return True
        except Exception as e:
            print(f"✗ FALLIDO: {str(e)}")
            self.tests_fallidos += 1
            return False
    
    def test_eliminar_producto(self):
        """Test: Eliminar producto."""
        print("\n[TEST 6] Eliminar Producto...")
        try:
            producto = GestorInventario.crear_producto('Delete Test', 5.00, 5)
            producto_id = producto.id
            
            resultado = GestorInventario.eliminar_producto(producto_id)
            assert resultado == True, "No se eliminó el producto"
            
            obtenido = GestorInventario.obtener_por_id(producto_id)
            assert obtenido is None, "Producto aún existe después de eliminarse"
            
            print("✓ PASADO: Producto eliminado correctamente")
            self.tests_pasados += 1
            return True
        except Exception as e:
            print(f"✗ FALLIDO: {str(e)}")
            self.tests_fallidos += 1
            return False
    
    def test_obtener_bajo_stock(self):
        """Test: Obtener productos con bajo stock."""
        print("\n[TEST 7] Obtener Productos Bajo Stock...")
        try:
            GestorInventario.crear_producto('Alto Stock', 5.00, 50)
            GestorInventario.crear_producto('Bajo Stock 1', 5.00, 3)
            GestorInventario.crear_producto('Bajo Stock 2', 5.00, 2)
            
            bajo_stock = GestorInventario.obtener_bajo_stock(cantidad_minima=10)
            assert len(bajo_stock) >= 2, "No se encontraron productos con bajo stock"
            
            print(f"✓ PASADO: Se encontraron {len(bajo_stock)} productos con bajo stock")
            self.tests_pasados += 1
            return True
        except Exception as e:
            print(f"✗ FALLIDO: {str(e)}")
            self.tests_fallidos += 1
            return False
    
    def test_estadisticas(self):
        """Test: Obtener estadísticas."""
        print("\n[TEST 8] Obtener Estadísticas...")
        try:
            GestorInventario.crear_producto('Stat 1', 10.00, 5)
            GestorInventario.crear_producto('Stat 2', 20.00, 3)
            
            stats = GestorInventario.obtener_estadisticas()
            
            assert 'total_productos' in stats, "Falta total_productos"
            assert 'valor_total' in stats, "Falta valor_total"
            assert 'precio_promedio' in stats, "Falta precio_promedio"
            
            print(f"✓ PASADO: Estadísticas obtenidas (Total: {stats['total_productos']} productos)")
            self.tests_pasados += 1
            return True
        except Exception as e:
            print(f"✗ FALLIDO: {str(e)}")
            self.tests_fallidos += 1
            return False
    
    def test_validacion(self):
        """Test: Validar datos."""
        print("\n[TEST 9] Validación de Datos...")
        try:
            # Válido
            es_valido, _ = GestorInventario.validar_producto('Producto', 5.00, 10)
            assert es_valido == True, "Validación correcta falló"
            
            # Inválido - precio negativo
            es_valido, _ = GestorInventario.validar_producto('Producto', -5.00, 10)
            assert es_valido == False, "No validó precio negativo"
            
            # Inválido - cantidad negativa
            es_valido, _ = GestorInventario.validar_producto('Producto', 5.00, -10)
            assert es_valido == False, "No validó cantidad negativa"
            
            print("✓ PASADO: Todas las validaciones funcionan correctamente")
            self.tests_pasados += 1
            return True
        except Exception as e:
            print(f"✗ FALLIDO: {str(e)}")
            self.tests_fallidos += 1
            return False
    
    def test_persistencia_json(self):
        """Test: Persistencia en JSON."""
        print("\n[TEST 10] Persistencia en JSON...")
        try:
            GestorInventario.crear_producto('JSON Test', 9.00, 7)
            
            datos_json = read_json()
            assert len(datos_json) > 0, "No hay datos en JSON"
            assert any(d.get('nombre') == 'JSON Test' for d in datos_json), "Producto no encontrado en JSON"
            
            print(f"✓ PASADO: JSON contiene {len(datos_json)} registros")
            self.tests_pasados += 1
            return True
        except Exception as e:
            print(f"✗ FALLIDO: {str(e)}")
            self.tests_fallidos += 1
            return False
    
    def test_persistencia_csv(self):
        """Test: Persistencia en CSV."""
        print("\n[TEST 11] Persistencia en CSV...")
        try:
            GestorInventario.crear_producto('CSV Test', 8.00, 6)
            
            datos_csv = read_csv()
            assert len(datos_csv) > 0, "No hay datos en CSV"
            
            print(f"✓ PASADO: CSV contiene {len(datos_csv)} registros")
            self.tests_pasados += 1
            return True
        except Exception as e:
            print(f"✗ FALLIDO: {str(e)}")
            self.tests_fallidos += 1
            return False
    
    def test_persistencia_txt(self):
        """Test: Persistencia en TXT."""
        print("\n[TEST 12] Persistencia en TXT...")
        try:
            GestorInventario.crear_producto('TXT Test', 7.50, 4)
            
            datos_txt = read_txt()
            assert len(datos_txt) > 0, "No hay datos en TXT"
            
            print(f"✓ PASADO: TXT contiene {len(datos_txt)} registros")
            self.tests_pasados += 1
            return True
        except Exception as e:
            print(f"✗ FALLIDO: {str(e)}")
            self.tests_fallidos += 1
            return False
    
    def test_to_dict(self):
        """Test: Convertir Producto a diccionario."""
        print("\n[TEST 13] Conversión ORM a Diccionario...")
        try:
            producto = GestorInventario.crear_producto('Dict Test', 6.00, 12)
            
            dict_producto = producto.to_dict()
            assert isinstance(dict_producto, dict), "No se convirtió a diccionario"
            assert 'nombre' in dict_producto, "Falta campo 'nombre'"
            assert 'fecha_creacion' in dict_producto, "Falta campo 'fecha_creacion'"
            
            print("✓ PASADO: Objeto Producto convertido correctamente a diccionario")
            self.tests_pasados += 1
            return True
        except Exception as e:
            print(f"✗ FALLIDO: {str(e)}")
            self.tests_fallidos += 1
            return False
    
    def ejecutar_todos(self):
        """Ejecuta todos los tests."""
        print("\n" + "=" * 70)
        print("EJECUTANDO TESTS - SEMANA 12: PERSISTENCIA DE DATOS")
        print("=" * 70)
        
        self.limpiar_base_datos()
        
        self.test_crear_producto()
        self.test_obtener_todos()
        self.test_obtener_por_id()
        self.test_obtener_por_nombre()
        self.test_actualizar_producto()
        self.test_eliminar_producto()
        self.test_obtener_bajo_stock()
        self.test_estadisticas()
        self.test_validacion()
        self.test_persistencia_json()
        self.test_persistencia_csv()
        self.test_persistencia_txt()
        self.test_to_dict()
        
        self.mostrar_resumen()
        
        self.app_context.pop()
    
    def mostrar_resumen(self):
        """Muestra resumen de los tests."""
        total = self.tests_pasados + self.tests_fallidos
        
        print("\n" + "=" * 70)
        print("RESUMEN DE TESTS")
        print("=" * 70)
        print(f"Total de tests: {total}")
        print(f"✓ Pasados: {self.tests_pasados}")
        print(f"✗ Fallidos: {self.tests_fallidos}")
        
        if self.tests_fallidos == 0:
            print("\n🎉 ¡TODOS LOS TESTS PASARON EXITOSAMENTE!")
        else:
            print(f"\n⚠️  {self.tests_fallidos} test(s) fallaron")
        
        print("=" * 70 + "\n")


if __name__ == '__main__':
    test = TestSemana12()
    test.ejecutar_todos()
