"""
main.py
=======

Punto de entrada del Sistema de Gestión de Bodega (POO Semanas 5 y 6).

Autor: Luis Alberto Villegas Merchan

Uso:
- Ejecución con interfaz gráfica (Flet):
    python main.py
- Ejecución de demostración y pruebas en consola:
    python main.py --cli
"""

from __future__ import annotations

import sys

import flet as ft

from app import crear_aplicacion
from modelo import CatalogoProductos, Categoria, Producto


def ejecutar_demostracion_consola() -> None:
    """Demuestra las operaciones CRUD con colecciones (list, dict, set) en consola."""
    print("=" * 70)
    print("   SISTEMA DE GESTIÓN DE BODEGA | POO SEMANA 5: COLECCIONES Y CRUD")
    print("=" * 70)
    print("Autor: Luis Alberto Villegas Merchan")
    print("Colecciones implementadas: set (unicidad), dict (índice O(1)), list (orden)\n")

    catalogo = CatalogoProductos()

    # 1. Crear categorías
    cat_acc = Categoria("CAT-ACC", "Accesorios")
    cat_elec = Categoria("CAT-ELE", "Electrónica")

    # 2. CREATE / AGREGAR
    print("[1] Operación CREATE: Agregando productos al catálogo...")
    p1 = Producto("PRD-001", "Lector Óptico Láser RF", 145.00, 20, cat_acc)
    p2 = Producto("PRD-002", "Terminal Portátil Android", 380.00, 10, cat_elec)
    catalogo.agregar_producto(p1)
    catalogo.agregar_producto(p2)
    print(f"[OK] {p1.mostrar_informacion()}")
    print(f"[OK] {p2.mostrar_informacion()}")

    # 3. Evitar Duplicados (SET)
    print("\n[2] Validación de Unicidad con 'set' (Evitar Duplicados):")
    try:
        p_duplicado = Producto("PRD-001", "Lector Clonado", 100.00, 5, cat_acc)
        catalogo.agregar_producto(p_duplicado)
    except ValueError as e:
        print("[OK] El 'set' interceptó y bloqueó el código duplicado:")
        print(f"     Mensaje: {e}")

    # 4. READ / BUSCAR
    print("\n[3] Operación READ: Búsqueda O(1) con 'dict' y por coincidencia en 'list':")
    busqueda_codigo = catalogo.buscar_por_codigo("PRD-002")
    if busqueda_codigo:
        print(f"[OK] Búsqueda por código 'PRD-002' encontrada: {busqueda_codigo.get_nombre()}")

    busqueda_nombre = catalogo.buscar_por_nombre("Lector")
    print(f"[OK] Búsqueda parcial 'Lector': {len(busqueda_nombre)} producto(s) encontrado(s).")

    # 5. UPDATE / ACTUALIZAR
    print("\n[4] Operación UPDATE: Actualizando precio y stock de PRD-001...")
    catalogo.actualizar_producto("PRD-001", "Lector Óptico Láser RF Pro", 160.00, 35, cat_acc)
    prod_actualizado = catalogo.buscar_por_codigo("PRD-001")
    if prod_actualizado:
        print(f"[OK] Nuevo nombre: {prod_actualizado.get_nombre()}")
        print(f"[OK] Nuevo precio: ${prod_actualizado.get_precio():,.2f} | Nuevo stock: {prod_actualizado.get_stock()} uds.")

    # 6. DELETE / ELIMINAR
    print("\n[5] Operación DELETE: Eliminando producto PRD-002...")
    catalogo.eliminar_producto("PRD-002")
    print("[OK] Producto 'PRD-002' eliminado de set, dict y list.")
    print(f"[OK] Total productos restantes en catálogo: {catalogo.total_productos()}")

    # 7. MÉTRICAS
    print("\n[6] Métricas del Inventario:")
    print(f"    Total Productos: {catalogo.total_productos()}")
    print(f"    Total Unidades en Stock: {catalogo.total_unidades_stock()} uds.")
    print(f"    Valor Total del Inventario: ${catalogo.valor_total_inventario():,.2f}")

    print("\n" + "=" * 70)
    print("   TODAS LAS PRUEBAS DE COLECCIONES Y CRUD FINALIZADAS CON ÉXITO")
    print("=" * 70)


def main() -> None:
    """Punto de entrada principal."""
    if len(sys.argv) > 1 and sys.argv[1].lower() in ("--cli", "-c", "--test"):
        ejecutar_demostracion_consola()
    else:
        # Lanza la interfaz gráfica en Flet
        ft.app(target=crear_aplicacion)


if __name__ == "__main__":
    main()
