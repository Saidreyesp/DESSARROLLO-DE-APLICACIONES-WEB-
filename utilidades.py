#!/usr/bin/env python3
"""
Script de Utilidades para Semana 12 - Herramientas Auxiliares

Proporciona funciones de utilidad para operaciones comunes en el sistema
de inventario, incluyendo respaldo, restauración y mantenimiento.
"""

import os
import json
import shutil
from datetime import datetime
from pathlib import Path


class UtilInventario:
    """Clase con funciones de utilidad para el sistema de inventario."""
    
    DATA_DIR = Path(__file__).parent / 'inventario' / 'data'
    DB_FILE = Path(__file__).parent / 'inventario.db'
    BACKUP_DIR = Path(__file__).parent / 'backups'
    
    @classmethod
    def crear_backup(cls):
        """Crea un respaldo de la base de datos y archivos de datos."""
        print("\n[RESPALDO] Creando respaldo de datos...")
        
        try:
            cls.BACKUP_DIR.mkdir(exist_ok=True)
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_subdir = cls.BACKUP_DIR / f'backup_{timestamp}'
            backup_subdir.mkdir()
            
            # Respaldo de base de datos
            if cls.DB_FILE.exists():
                shutil.copy2(cls.DB_FILE, backup_subdir / 'inventario.db')
                print(f"  ✓ Base de datos: {cls.DB_FILE.name}")
            
            # Respaldo de archivos de datos
            for archivo in ['datos.txt', 'datos.json', 'datos.csv']:
                origen = cls.DATA_DIR / archivo
                if origen.exists():
                    shutil.copy2(origen, backup_subdir / archivo)
                    print(f"  ✓ Archivo: {archivo}")
            
            print(f"✓ Respaldo completado en: {backup_subdir}")
            return backup_subdir
        
        except Exception as e:
            print(f"✗ Error al crear respaldo: {e}")
            return None
    
    @classmethod
    def limpiar_datos(cls):
        """Limpia todos los archivos de datos (cuidado, no recuperable)."""
        print("\n[LIMPIEZA] Limpiando datos...")
        
        confirmar = input("⚠️  Esto eliminará todos los datos de archivos. ¿Continuar? (s/n): ")
        if confirmar.lower() != 's':
            print("Operación cancelada")
            return False
        
        try:
            # Limpiar archivos de datos
            datos_txt = cls.DATA_DIR / 'datos.txt'
            datos_json = cls.DATA_DIR / 'datos.json'
            datos_csv = cls.DATA_DIR / 'datos.csv'
            
            if datos_txt.exists():
                datos_txt.write_text('')
                print("  ✓ datos.txt limpiado")
            
            if datos_json.exists():
                datos_json.write_text('[]')
                print("  ✓ datos.json limpiado")
            
            if datos_csv.exists():
                datos_csv.write_text('nombre,precio,cantidad\n')
                print("  ✓ datos.csv limpiado")
            
            print("✓ Datos limpios")
            return True
        
        except Exception as e:
            print(f"✗ Error al limpiar datos: {e}")
            return False
    
    @classmethod
    def info_sistema(cls):
        """Muestra información general del sistema."""
        print("\n[INFO] Información del Sistema de Inventario")
        print("=" * 60)
        
        # Base de datos
        if cls.DB_FILE.exists():
            db_size = cls.DB_FILE.stat().st_size / 1024  # KB
            print(f"Base de Datos: {cls.DB_FILE.name}")
            print(f"  Tamaño: {db_size:.2f} KB")
        else:
            print(f"Base de Datos: No existe")
        
        # Archivos de datos
        print(f"\nArchivos de Datos ({cls.DATA_DIR.name}):")
        for archivo in ['datos.txt', 'datos.json', 'datos.csv']:
            ruta = cls.DATA_DIR / archivo
            if ruta.exists():
                tamaño = ruta.stat().st_size / 1024  # KB
                líneas = len(ruta.read_text().splitlines())
                print(f"  {archivo}: {tamaño:.2f} KB ({líneas} líneas)")
            else:
                print(f"  {archivo}: No existe")
        
        # Backups
        if cls.BACKUP_DIR.exists():
            backups = list(cls.BACKUP_DIR.glob('backup_*'))
            print(f"\nRespaldos (Backups): {len(backups)}")
            for backup in backups[-5:]:  # Últimos 5
                print(f"  - {backup.name}")
        
        print("=" * 60)
    
    @classmethod
    def sincronizar_archivos(cls):
        """Sincroniza archivos de datos (comprueba integridad)."""
        print("\n[SINCRONIZACIÓN] Verificando integridad de archivos...")
        
        try:
            datos_dir = cls.DATA_DIR
            datos_dir.mkdir(exist_ok=True)
            
            archivos = {
                'datos.txt': '',
                'datos.json': '[]',
                'datos.csv': 'nombre,precio,cantidad\n'
            }
            
            for archivo, contenido_default in archivos.items():
                ruta = datos_dir / archivo
                
                if not ruta.exists():
                    ruta.write_text(contenido_default)
                    print(f"  ✓ Creado: {archivo}")
                else:
                    # Verificar que tenga contenido
                    contenido = ruta.read_text()
                    if not contenido or contenido.isspace():
                        ruta.write_text(contenido_default)
                        print(f"  ⚠️  Restaurado: {archivo}")
                    else:
                        print(f"  ✓ OK: {archivo}")
            
            print("✓ Sincronización completada")
            return True
        
        except Exception as e:
            print(f"✗ Error en sincronización: {e}")
            return False
    
    @classmethod
    def restaurar_backup(cls, numero_backup=0):
        """Restaura un respaldo anterior."""
        print(f"\n[RESTAURACIÓN] Listando respaldos...")
        
        try:
            if not cls.BACKUP_DIR.exists():
                print("No hay respaldos disponibles")
                return False
            
            backups = sorted(cls.BACKUP_DIR.glob('backup_*'), reverse=True)
            
            if not backups:
                print("No hay respaldos disponibles")
                return False
            
            print("Respaldos disponibles:")
            for i, backup in enumerate(backups):
                print(f"  {i}: {backup.name}")
            
            # Seleccionar backup
            seleccion = input(f"\nSelecciona backup (0-{len(backups)-1}): ")
            try:
                indice = int(seleccion)
                backup_seleccionado = backups[indice]
            except (ValueError, IndexError):
                print("Selección inválida")
                return False
            
            # Confirmar
            confirmar = input(f"\n¿Restaurar {backup_seleccionado.name}? (s/n): ")
            if confirmar.lower() != 's':
                print("Operación cancelada")
                return False
            
            # Restaurar
            for archivo in ['inventario.db', 'datos.txt', 'datos.json', 'datos.csv']:
                origen = backup_seleccionado / archivo
                
                if archivo == 'inventario.db':
                    destino = cls.DB_FILE
                else:
                    destino = cls.DATA_DIR / archivo
                
                if origen.exists():
                    shutil.copy2(origen, destino)
                    print(f"  ✓ Restaurado: {archivo}")
            
            print("✓ Restauración completada")
            return True
        
        except Exception as e:
            print(f"✗ Error en restauración: {e}")
            return False
    
    @classmethod
    def limpiar_backups_antiguos(cls, dias=30):
        """Limpia respaldos más antiguos que el número de días especificado."""
        print(f"\n[LIMPIEZA] Removiendo respaldos más ancianos de {dias} días...")
        
        if not cls.BACKUP_DIR.exists():
            print("No hay respaldos para limpiar")
            return True
        
        try:
            from datetime import timedelta
            fecha_limite = datetime.now() - timedelta(days=dias)
            
            backups_removidos = 0
            for backup in cls.BACKUP_DIR.glob('backup_*'):
                if backup.is_dir():
                    # Obtener fecha del nombre (backup_YYYYMMDD_HHMMSS)
                    try:
                        fecha_str = backup.name.split('_')[1] + ' ' + backup.name.split('_')[2]
                        fecha_backup = datetime.strptime(fecha_str, '%Y%m%d %H%M%S')
                        
                        if fecha_backup < fecha_limite:
                            shutil.rmtree(backup)
                            print(f"  ✓ Removido: {backup.name}")
                            backups_removidos += 1
                    except:
                        pass
            
            print(f"✓ Limpieza completada ({backups_removidos} respaldos removidos)")
            return True
        
        except Exception as e:
            print(f"✗ Error en limpieza: {e}")
            return False
    
    @classmethod
    def exportar_datos(cls, formato='json', archivo_salida=None):
        """Exporta datos a un archivo externo."""
        print(f"\n[EXPORTACIÓN] Exportando datos a formato {formato.upper()}...")
        
        try:
            if not archivo_salida:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                archivo_salida = Path(__file__).parent / f'export_{timestamp}.{formato}'
            else:
                archivo_salida = Path(archivo_salida)
            
            # Leer datos de múltiples fuentes
            datos_json = cls.DATA_DIR / 'datos.json'
            
            if datos_json.exists():
                contenido = datos_json.read_text()
                datos = json.loads(contenido) if contenido else []
            else:
                datos = []
            
            # Exportar según formato
            if formato.lower() == 'json':
                with open(archivo_salida, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, ensure_ascii=False, indent=2)
            
            elif formato.lower() == 'csv':
                import csv
                if datos:
                    with open(archivo_salida, 'w', newline='', encoding='utf-8') as f:
                        writer = csv.DictWriter(f, fieldnames=datos[0].keys())
                        writer.writeheader()
                        writer.writerows(datos)
            
            print(f"✓ Exportación completada: {archivo_salida}")
            print(f"  Registros: {len(datos)}")
            return archivo_salida
        
        except Exception as e:
            print(f"✗ Error en exportación: {e}")
            return None
    
    @classmethod
    def menu_principal(cls):
        """Muestra menú interactivo."""
        while True:
            print("\n" + "=" * 60)
            print("UTILIDADES DE INVENTARIO - SEMANA 12")
            print("=" * 60)
            print("1. Ver información del sistema")
            print("2. Crear respaldo")
            print("3. Restaurar respaldo")
            print("4. Sincronizar archivos")
            print("5. Exportar datos")
            print("6. Limpiar respaldos antiguos")
            print("7. Limpiar datos (⚠️ irreversible)")
            print("0. Salir")
            print("-" * 60)
            
            opcion = input("Selecciona una opción: ").strip()
            
            if opcion == '1':
                cls.info_sistema()
            elif opcion == '2':
                cls.crear_backup()
            elif opcion == '3':
                cls.restaurar_backup()
            elif opcion == '4':
                cls.sincronizar_archivos()
            elif opcion == '5':
                formato = input("Formato (json/csv): ").strip().lower() or 'json'
                cls.exportar_datos(formato=formato)
            elif opcion == '6':
                dias = int(input("Días (default 30): ") or 30)
                cls.limpiar_backups_antiguos(dias=dias)
            elif opcion == '7':
                cls.limpiar_datos()
            elif opcion == '0':
                print("\nSaliendo...")
                break
            else:
                print("Opción inválida")


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1:
        comando = sys.argv[1].lower()
        
        if comando == 'backup':
            UtilInventario.crear_backup()
        elif comando == 'restore':
            UtilInventario.restaurar_backup()
        elif comando == 'sync':
            UtilInventario.sincronizar_archivos()
        elif comando == 'info':
            UtilInventario.info_sistema()
        elif comando == 'export':
            formato = sys.argv[2] if len(sys.argv) > 2 else 'json'
            UtilInventario.exportar_datos(formato=formato)
        elif comando == 'clean-backups':
            dias = int(sys.argv[2]) if len(sys.argv) > 2 else 30
            UtilInventario.limpiar_backups_antiguos(dias=dias)
        else:
            print(f"Comando desconocido: {comando}")
    else:
        UtilInventario.menu_principal()
