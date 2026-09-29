"""
test_modelo.py
==============

Pruebas unitarias para las entidades del dominio y validaciones con Pydantic.

Autor: Luis Alberto Villegas Merchan
Actividad: Semana 7 — Patrones de Diseño, Testing Unitario y TDAs Lineales
"""

import pytest
from modelo import Categoria, PedidoDespacho, Producto
from pydantic import ValidationError


class TestModeloDominio:
    """Pruebas de inicialización y validación de reglas de negocio."""

    def test_creacion_categoria_valida(self):
        cat = Categoria("CAT-RED", "Redes")
        assert cat.get_codigo() == "CAT-RED"
        assert cat.get_nombre() == "Redes"

    def test_creacion_categoria_invalida(self):
        with pytest.raises(ValidationError):
            Categoria("C", "A")  # longitud menor a 2

    def test_creacion_producto_valido(self):
        cat = Categoria("CAT-ACC", "Accesorios")
        prod = Producto("PRD-001", "Mouse Óptico", 25.50, 15, cat)
        assert prod.get_codigo() == "PRD-001"
        assert prod.get_precio() == 25.50
        assert prod.get_stock() == 15
        assert prod.calcular_valor_inventario() == 25.50 * 15

    def test_producto_precio_invalido(self):
        cat = Categoria("CAT-ACC", "Accesorios")
        with pytest.raises(ValidationError):
            Producto("PRD-001", "Mouse", -10.0, 10, cat)  # Precio negativo

    def test_producto_stock_invalido(self):
        cat = Categoria("CAT-ACC", "Accesorios")
        with pytest.raises(ValidationError):
            Producto("PRD-001", "Mouse", 10.0, -5, cat)  # Stock negativo

    def test_aumentar_y_disminuir_stock(self):
        cat = Categoria("CAT-ACC", "Accesorios")
        prod = Producto("PRD-001", "Mouse", 10.0, 20, cat)

        prod.aumentar_stock(10)
        assert prod.get_stock() == 30

        prod.disminuir_stock(15)
        assert prod.get_stock() == 15

        with pytest.raises(ValueError, match="Stock insuficiente"):
            prod.disminuir_stock(50)

    def test_pedido_despacho_valido(self):
        pedido = PedidoDespacho(
            id_pedido="PED-001",
            cliente="Logística Norte",
            codigo_producto="PRD-001",
            nombre_producto="Mouse",
            cantidad=5,
        )
        assert pedido.get_id_pedido() == "PED-001"
        assert pedido.get_cliente() == "Logística Norte"
        assert pedido.get_cantidad() == 5
        assert pedido.get_estado() == "PENDIENTE"

        pedido.marcar_despachado()
        assert pedido.get_estado() == "DESPACHADO"

    def test_pedido_despacho_cantidad_invalida(self):
        with pytest.raises(ValidationError):
            PedidoDespacho(
                id_pedido="PED-002",
                cliente="Logística Sur",
                codigo_producto="PRD-001",
                nombre_producto="Mouse",
                cantidad=0,  # gt=0 requerido
            )
