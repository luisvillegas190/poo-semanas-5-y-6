"""
test_estructuras_lineales.py
============================

Pruebas unitarias con Pytest para las estructuras lineales implementadas manualmente:
- ColaLineal (FIFO)
- PilaLineal (LIFO)

Autor: Luis Alberto Villegas Merchan
Actividad: Semana 7 — Testing Unitario de Tipos de Datos Abstractos Lineales
"""

import pytest
from estructuras_lineales import ColaLineal, ColaVaciaError, PilaLineal, PilaVaciaError


# ==========================================
# 1. PRUEBAS PARA COLA LINEAL (QUEUE - FIFO)
# ==========================================

class TestColaLineal:
    """Conjunto de pruebas para la estructura ColaLineal."""

    def test_inicializacion_cola_vacia(self):
        """Verifica que una cola nueva se cree vacía y con longitud 0."""
        cola: ColaLineal[int] = ColaLineal()
        assert cola.esta_vacia() is True
        assert cola.tamano() == 0
        assert len(cola) == 0
        assert cola.a_lista() == []

    def test_encolar_un_elemento(self):
        """Verifica el encolado de un único elemento."""
        cola: ColaLineal[str] = ColaLineal()
        cola.encolar("Elemento-1")

        assert cola.esta_vacia() is False
        assert cola.tamano() == 1
        assert len(cola) == 1
        assert cola.ver_frente() == "Elemento-1"

    def test_encolar_multiples_y_orden_fifo(self):
        """
        Verifica el comportamiento FIFO (First-In, First-Out):
        Los elementos deben salir en el mismo orden exacto en el que entraron.
        """
        cola: ColaLineal[int] = ColaLineal()
        elementos = [10, 20, 30, 40, 50]

        for item in elementos:
            cola.encolar(item)

        assert cola.tamano() == 5
        assert cola.ver_frente() == 10

        desencolados = []
        while not cola.esta_vacia():
            desencolados.append(cola.desencolar())

        assert desencolados == [10, 20, 30, 40, 50]
        assert cola.esta_vacia() is True
        assert cola.tamano() == 0

    def test_ver_frente_no_altera_la_estructura(self):
        """Verifica que ver_frente (peek) sea idempotente y no remueva elementos."""
        cola: ColaLineal[str] = ColaLineal()
        cola.encolar("Primero")
        cola.encolar("Segundo")

        assert cola.ver_frente() == "Primero"
        assert cola.ver_frente() == "Primero"
        assert cola.tamano() == 2
        assert cola.desencolar() == "Primero"
        assert cola.ver_frente() == "Segundo"

    def test_desencolar_en_cola_vacia_lanza_excepcion(self):
        """Verifica que desencolar en una cola vacía dispare ColaVaciaError."""
        cola: ColaLineal[str] = ColaLineal()
        with pytest.raises(ColaVaciaError, match="la cola está vacía"):
            cola.desencolar()

    def test_ver_frente_en_cola_vacia_lanza_excepcion(self):
        """Verifica que ver_frente en una cola vacía dispare ColaVaciaError."""
        cola: ColaLineal[float] = ColaLineal()
        with pytest.raises(ColaVaciaError, match="la cola está vacía"):
            cola.ver_frente()

    def test_limpiar_cola(self):
        """Verifica que limpiar() reinicie completamente la cola."""
        cola: ColaLineal[int] = ColaLineal()
        cola.encolar(1)
        cola.encolar(2)
        cola.limpiar()

        assert cola.esta_vacia() is True
        assert cola.tamano() == 0
        assert len(cola) == 0

    def test_iteracion_y_a_lista(self):
        """Verifica la exportación a lista e iterador sin corromper la cola."""
        cola: ColaLineal[str] = ColaLineal()
        cola.encolar("A")
        cola.encolar("B")
        cola.encolar("C")

        assert cola.a_lista() == ["A", "B", "C"]
        assert list(cola) == ["A", "B", "C"]
        # La cola original debe mantener su estado intacto
        assert cola.tamano() == 3


# ==========================================
# 2. PRUEBAS PARA PILA LINEAL (STACK - LIFO)
# ==========================================

class TestPilaLineal:
    """Conjunto de pruebas para la estructura PilaLineal."""

    def test_inicializacion_pila_vacia(self):
        """Verifica que una pila nueva inicie vacía."""
        pila: PilaLineal[int] = PilaLineal()
        assert pila.esta_vacia() is True
        assert pila.tamano() == 0
        assert len(pila) == 0
        assert pila.a_lista() == []

    def test_apilar_y_desapilar_orden_lifo(self):
        """
        Verifica el comportamiento LIFO (Last-In, First-Out):
        El último elemento insertado debe ser el primero en salir.
        """
        pila: PilaLineal[str] = PilaLineal()
        pila.apilar("Fondo")
        pila.apilar("Medio")
        pila.apilar("Tope")

        assert pila.tamano() == 3
        assert pila.ver_tope() == "Tope"

        assert pila.desapilar() == "Tope"
        assert pila.ver_tope() == "Medio"

        assert pila.desapilar() == "Medio"
        assert pila.desapilar() == "Fondo"

        assert pila.esta_vacia() is True

    def test_desapilar_en_pila_vacia_lanza_excepcion(self):
        """Verifica que desapilar en pila vacía lance PilaVaciaError."""
        pila: PilaLineal[int] = PilaLineal()
        with pytest.raises(PilaVaciaError, match="la pila está vacía"):
            pila.desapilar()

    def test_ver_tope_en_pila_vacia_lanza_excepcion(self):
        """Verifica que ver_tope en pila vacía lance PilaVaciaError."""
        pila: PilaLineal[str] = PilaLineal()
        with pytest.raises(PilaVaciaError, match="la pila está vacía"):
            pila.ver_tope()
