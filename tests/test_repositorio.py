"""
test_repositorio.py
===================

Pruebas unitarias con Pytest para el patrón de diseño Repository:
- ProductoRepositoryMemoria (CRUD e inventario)
- DespachoColaRepository (Integración con ColaLineal manual FIFO y control de stock)

Autor: Luis Alberto Villegas Merchan
Actividad: Semana 7 — Patrones de Diseño y Testing Unitario
"""

import pytest
from estructuras_lineales import ColaVaciaError
from modelo import Categoria, PedidoDespacho, Producto
from repositorio import DespachoColaRepository, ProductoRepositoryMemoria


@pytest.fixture
def categoria_prueba() -> Categoria:
    return Categoria("CAT-TEST", "Tecnología de Prueba")


@pytest.fixture
def repo_productos(categoria_prueba: Categoria) -> ProductoRepositoryMemoria:
    """Fixture que provee un repositorio de productos con datos limpios."""
    repo = ProductoRepositoryMemoria()
    p1 = Producto("PRD-101", "Sensor Infrarrojo", 50.0, 20, categoria_prueba)
    p2 = Producto("PRD-102", "Controlador PLC", 200.0, 5, categoria_prueba)
    repo.guardar(p1)
    repo.guardar(p2)
    return repo


class TestProductoRepositoryMemoria:
    """Pruebas para ProductoRepositoryMemoria (CRUD y Métricas)."""

    def test_guardar_y_obtener_por_codigo(self, repo_productos: ProductoRepositoryMemoria):
        producto = repo_productos.obtener_por_codigo("PRD-101")
        assert producto is not None
        assert producto.get_nombre() == "Sensor Infrarrojo"
        assert producto.get_stock() == 20

    def test_evitar_codigo_duplicado(
        self, repo_productos: ProductoRepositoryMemoria, categoria_prueba: Categoria
    ):
        """Verifica que no se permita registrar dos productos con el mismo código."""
        clon = Producto("PRD-101", "Sensor Clonado", 60.0, 10, categoria_prueba)
        with pytest.raises(ValueError, match="ya está registrado"):
            repo_productos.guardar(clon)

    def test_actualizar_producto(
        self, repo_productos: ProductoRepositoryMemoria, categoria_prueba: Categoria
    ):
        repo_productos.actualizar(
            codigo="PRD-101",
            nombre="Sensor Infrarrojo V2",
            precio=55.0,
            stock=30,
            categoria=categoria_prueba,
        )
        actualizado = repo_productos.obtener_por_codigo("PRD-101")
        assert actualizado is not None
        assert actualizado.get_nombre() == "Sensor Infrarrojo V2"
        assert actualizado.get_precio() == 55.0
        assert actualizado.get_stock() == 30

    def test_actualizar_inexistente_lanza_error(
        self, repo_productos: ProductoRepositoryMemoria, categoria_prueba: Categoria
    ):
        with pytest.raises(KeyError, match="No existe ningún producto"):
            repo_productos.actualizar(
                codigo="PRD-999",
                nombre="Fantasma",
                precio=10.0,
                stock=1,
                categoria=categoria_prueba,
            )

    def test_eliminar_producto(self, repo_productos: ProductoRepositoryMemoria):
        assert repo_productos.contar() == 2
        repo_productos.eliminar("PRD-101")
        assert repo_productos.contar() == 1
        assert repo_productos.obtener_por_codigo("PRD-101") is None

    def test_eliminar_inexistente_lanza_error(self, repo_productos: ProductoRepositoryMemoria):
        with pytest.raises(KeyError, match="no existe"):
            repo_productos.eliminar("PRD-INEXISTENTE")

    def test_metricas_globales(self, repo_productos: ProductoRepositoryMemoria):
        # PRD-101: 50 * 20 = 1000; PRD-102: 200 * 5 = 1000 => Total = 2000
        assert repo_productos.contar() == 2
        assert repo_productos.total_unidades() == 25
        assert repo_productos.valor_total() == 2000.0


class TestDespachoColaRepository:
    """Pruebas para DespachoColaRepository e integración con ColaLineal manual."""

    def test_encolar_pedido_exitoso(self, repo_productos: ProductoRepositoryMemoria):
        repo_despacho = DespachoColaRepository(producto_repo=repo_productos)
        pedido = PedidoDespacho(
            id_pedido="ORD-001",
            cliente="Empresa Alfa",
            codigo_producto="PRD-101",
            nombre_producto="Sensor Infrarrojo",
            cantidad=5,
        )
        repo_despacho.encolar_despacho(pedido)

        assert repo_despacho.total_pendientes() == 1
        assert repo_despacho.esta_vacio() is False
        assert repo_despacho.consultar_proximo().get_id_pedido() == "ORD-001"

    def test_encolar_producto_inexistente_falla(self, repo_productos: ProductoRepositoryMemoria):
        repo_despacho = DespachoColaRepository(producto_repo=repo_productos)
        pedido_invalido = PedidoDespacho(
            id_pedido="ORD-002",
            cliente="Empresa Beta",
            codigo_producto="PRD-999",  # No existe
            nombre_producto="Desconocido",
            cantidad=2,
        )
        with pytest.raises(KeyError, match="no existe en el catálogo"):
            repo_despacho.encolar_despacho(pedido_invalido)

    def test_encolar_stock_insuficiente_falla(self, repo_productos: ProductoRepositoryMemoria):
        repo_despacho = DespachoColaRepository(producto_repo=repo_productos)
        # PRD-102 tiene solo 5 unidades en stock
        pedido_excesivo = PedidoDespacho(
            id_pedido="ORD-003",
            cliente="Empresa Gamma",
            codigo_producto="PRD-102",
            nombre_producto="Controlador PLC",
            cantidad=10,  # Supera las 5 disponibles
        )
        with pytest.raises(ValueError, match="Stock insuficiente"):
            repo_despacho.encolar_despacho(pedido_excesivo)

    def test_despachar_orden_fifo_y_descontar_stock(
        self, repo_productos: ProductoRepositoryMemoria
    ):
        """
        Verifica que el despacho procese la orden más antigua (FIFO)
        y descuente correctamente las unidades físicas del inventario.
        """
        repo_despacho = DespachoColaRepository(producto_repo=repo_productos)

        pedido1 = PedidoDespacho(
            id_pedido="ORD-100",
            cliente="Cliente Primero",
            codigo_producto="PRD-101",
            nombre_producto="Sensor Infrarrojo",
            cantidad=4,
        )
        pedido2 = PedidoDespacho(
            id_pedido="ORD-200",
            cliente="Cliente Segundo",
            codigo_producto="PRD-101",
            nombre_producto="Sensor Infrarrojo",
            cantidad=6,
        )

        repo_despacho.encolar_despacho(pedido1)
        repo_despacho.encolar_despacho(pedido2)
        assert repo_despacho.total_pendientes() == 2

        # Despacho #1: Debe salir pedido1 (FIFO)
        despachado_1 = repo_despacho.despachar_siguiente()
        assert despachado_1.get_id_pedido() == "ORD-100"
        assert despachado_1.get_estado() == "DESPACHADO"
        # El stock inicial era 20, ahora debe ser 16
        prod = repo_productos.obtener_por_codigo("PRD-101")
        assert prod is not None
        assert prod.get_stock() == 16
        assert repo_despacho.total_pendientes() == 1

        # Despacho #2: Debe salir pedido2
        despachado_2 = repo_despacho.despachar_siguiente()
        assert despachado_2.get_id_pedido() == "ORD-200"
        assert prod.get_stock() == 10
        assert repo_despacho.total_pendientes() == 0
        assert repo_despacho.esta_vacio() is True

        # Historial de despachos debe tener ambos en orden LIFO
        historial = repo_despacho.listar_historial()
        assert len(historial) == 2
        assert historial[0].get_id_pedido() == "ORD-200"
        assert historial[1].get_id_pedido() == "ORD-100"

    def test_despachar_cola_vacia_lanza_error(self):
        repo_despacho = DespachoColaRepository()
        with pytest.raises(ColaVaciaError, match="No hay pedidos pendientes"):
            repo_despacho.despachar_siguiente()
