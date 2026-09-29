"""
estructuras_lineales.py
=======================

Implementación manual de Tipos de Datos Abstractos (TDA) Lineales:
- Cola (Queue - FIFO: First In, First Out)
- Pila (Stack - LIFO: Last In, First Out)

Actividad: Semana 7 — Patrones de Diseño, Testing Unitario y TDAs Lineales.
Materia: Programación Estructurada / Programación Orientada a Objetos
Estudiante: Luis Alberto Villegas Merchan

REQUISITO TÉCNICO CUMPLIDO:
Implementación manual basada en Nodos enlazados (Linked Nodes), SIN utilizar
directamente colecciones como 'collections.deque' o 'queue.Queue' del lenguaje.
Garantiza operaciones fundamentales en tiempo constante O(1).
"""

from __future__ import annotations

from typing import Generic, Iterator, Optional, TypeVar

T = TypeVar("T")


class EstructuraVaciaError(Exception):
    """Excepción base para operaciones inválidas en estructuras vacías."""


class ColaVaciaError(EstructuraVaciaError):
    """Lanzada cuando se intenta desencolar o consultar una cola vacía."""


class PilaVaciaError(EstructuraVaciaError):
    """Lanzada cuando se intenta desapilar o consultar una pila vacía."""


class Nodo(Generic[T]):
    """
    Representa un elemento individual en una estructura de datos enlazada.
    Almacena un dato de tipo genérico T y una referencia al siguiente nodo.
    """

    def __init__(self, dato: T, siguiente: Optional[Nodo[T]] = None) -> None:
        self.dato: T = dato
        self.siguiente: Optional[Nodo[T]] = siguiente

    def __repr__(self) -> str:
        return f"Nodo(dato={self.dato!r})"


class ColaLineal(Generic[T]):
    """
    Tipo de Dato Abstracto Lineal: COLA (Queue - FIFO).
    
    Política de acceso: El primer elemento en entrar es el primero en salir.
    Implementación: Lista simplemente enlazada con punteros al 'frente' y al 'final'.
    
    Complejidad temporal de las operaciones principales: O(1).
    """

    def __init__(self) -> None:
        """Inicializa una cola vacía con referencias nulas y contador en 0."""
        self.__frente: Optional[Nodo[T]] = None
        self.__final: Optional[Nodo[T]] = None
        self.__longitud: int = 0

    # 1. AGREGAR ELEMENTO (Enqueue)
    def encolar(self, elemento: T) -> None:
        """
        Inserta un nuevo elemento al final de la cola.
        Complejidad temporal: O(1).
        """
        nuevo_nodo = Nodo(elemento)
        if self.esta_vacia():
            self.__frente = nuevo_nodo
            self.__final = nuevo_nodo
        else:
            assert self.__final is not None
            self.__final.siguiente = nuevo_nodo
            self.__final = nuevo_nodo
        self.__longitud += 1

    # 2. ELIMINAR ELEMENTO (Dequeue)
    def desencolar(self) -> T:
        """
        Remueve y retorna el elemento situado al frente de la cola (FIFO).
        Complejidad temporal: O(1).
        
        Raises:
            ColaVaciaError: Si la cola no contiene elementos.
        """
        if self.esta_vacia():
            raise ColaVaciaError("No se puede desencolar: la cola está vacía.")

        assert self.__frente is not None
        nodo_removido = self.__frente
        self.__frente = self.__frente.siguiente
        self.__longitud -= 1

        # Si tras eliminar quedó vacía, se restablece el puntero final
        if self.__frente is None:
            self.__final = None

        return nodo_removido.dato

    # 3. CONSULTAR SIGUIENTE ELEMENTO (Peek / Front)
    def ver_frente(self) -> T:
        """
        Retorna el elemento al frente de la cola sin removerlo.
        Complejidad temporal: O(1).
        
        Raises:
            ColaVaciaError: Si la cola está vacía.
        """
        if self.esta_vacia():
            raise ColaVaciaError("No se puede consultar el frente: la cola está vacía.")
        assert self.__frente is not None
        return self.__frente.dato

    # 4. VERIFICAR SI ESTÁ VACÍA (IsEmpty)
    def esta_vacia(self) -> bool:
        """
        Indica si la estructura no contiene ningún elemento.
        Complejidad temporal: O(1).
        """
        return self.__frente is None

    # 5. CONSULTAR CANTIDAD DE ELEMENTOS (Size)
    def tamano(self) -> int:
        """
        Retorna la cantidad exacta de elementos almacenados.
        Complejidad temporal: O(1).
        """
        return self.__longitud

    def __len__(self) -> int:
        """Permite el uso de la función nativa len(cola)."""
        return self.tamano()

    def limpiar(self) -> None:
        """Vacía completamente la cola en tiempo O(1)."""
        self.__frente = None
        self.__final = None
        self.__longitud = 0

    def a_lista(self) -> list[T]:
        """
        Retorna una lista con los elementos desde el frente hasta el final.
        Útil para visualización en GUI sin alterar el estado de la cola.
        """
        elementos: list[T] = []
        actual = self.__frente
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def __iter__(self) -> Iterator[T]:
        """Permite iterar sobre los elementos de la cola en orden FIFO."""
        actual = self.__frente
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __repr__(self) -> str:
        items = " -> ".join(repr(x) for x in self.a_lista())
        return f"ColaLineal([{items}])"


class PilaLineal(Generic[T]):
    """
    Tipo de Dato Abstracto Lineal: PILA (Stack - LIFO).
    
    Política de acceso: El último elemento en entrar es el primero en salir.
    Implementación: Lista simplemente enlazada con puntero al 'tope'.
    
    Complejidad temporal de las operaciones principales: O(1).
    """

    def __init__(self) -> None:
        """Inicializa una pila vacía."""
        self.__tope: Optional[Nodo[T]] = None
        self.__longitud: int = 0

    # 1. AGREGAR ELEMENTO (Push)
    def apilar(self, elemento: T) -> None:
        """
        Inserta un nuevo elemento en la cima (tope) de la pila.
        Complejidad temporal: O(1).
        """
        nuevo_nodo = Nodo(elemento, siguiente=self.__tope)
        self.__tope = nuevo_nodo
        self.__longitud += 1

    # 2. ELIMINAR ELEMENTO (Pop)
    def desapilar(self) -> T:
        """
        Remueve y retorna el elemento situado en el tope de la pila (LIFO).
        Complejidad temporal: O(1).
        
        Raises:
            PilaVaciaError: Si la pila no contiene elementos.
        """
        if self.esta_vacia():
            raise PilaVaciaError("No se puede desapilar: la pila está vacía.")

        assert self.__tope is not None
        nodo_removido = self.__tope
        self.__tope = self.__tope.siguiente
        self.__longitud -= 1
        return nodo_removido.dato

    # 3. CONSULTAR TOPE (Peek)
    def ver_tope(self) -> T:
        """
        Retorna el elemento situado en el tope de la pila sin removerlo.
        Complejidad temporal: O(1).
        
        Raises:
            PilaVaciaError: Si la pila está vacía.
        """
        if self.esta_vacia():
            raise PilaVaciaError("No se puede consultar el tope: la pila está vacía.")
        assert self.__tope is not None
        return self.__tope.dato

    # 4. VERIFICAR SI ESTÁ VACÍA (IsEmpty)
    def esta_vacia(self) -> bool:
        """Indica si la pila no tiene elementos."""
        return self.__tope is None

    # 5. CONSULTAR CANTIDAD DE ELEMENTOS (Size)
    def tamano(self) -> int:
        """Retorna la cantidad de elementos almacenados."""
        return self.__longitud

    def __len__(self) -> int:
        return self.tamano()

    def limpiar(self) -> None:
        """Vacía la pila en tiempo O(1)."""
        self.__tope = None
        self.__longitud = 0

    def a_lista(self) -> list[T]:
        """Retorna los elementos desde el tope hacia la base."""
        elementos: list[T] = []
        actual = self.__tope
        while actual is not None:
            elementos.append(actual.dato)
            actual = actual.siguiente
        return elementos

    def __iter__(self) -> Iterator[T]:
        actual = self.__tope
        while actual is not None:
            yield actual.dato
            actual = actual.siguiente

    def __repr__(self) -> str:
        items = " | ".join(repr(x) for x in self.a_lista())
        return f"PilaLineal(tope -> [{items}])"
