"""
repositorio.py
==============

Implementación del Patrón de Diseño Repository (Repositorio).

Actividad: Semana 7 — Patrones de Diseño, Testing Unitario y TDAs Lineales.
Materia: Programación Estructurada / Programación Orientada a Objetos
Estudiante: Luis Alberto Villegas Merchan

PROPÓSITO DEL PATRÓN REPOSITORY:
Separar el acceso y persistencia de los datos de la lógica de negocio y de la
interfaz gráfica. Provee una interfaz limpia y desacoplada mediante clases base
abstractas (ABC) que define contratos estrictos.

INTEGRACIÓN REQUERIDA:
El repositorio de despachos ('DespachoColaRepository') integra directamente la
estructura de datos 'ColaLineal' implementada manualmente para gestionar las
solicitudes en estricto orden de llegada (FIFO). Adicionalmente integra 'PilaLineal'
para registrar el historial de auditoría de despachos completados (LIFO).
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional

from estructuras_lineales import ColaLineal, ColaVaciaError, PilaLineal
from modelo import Categoria, PedidoDespacho, Producto


# 1. INTERFAZ ABSTRACTA DEL REPOSITORIO DE PRODUCTOS

class IProductoRepository(ABC):
    """
    Contrato abstracto que define las operaciones de acceso y manipulación
    del inventario de productos.
    """

    @abstractmethod
    def guardar(self, producto: Producto) -> None:
        """Persiste un nuevo producto."""
        pass

    @abstractmethod
    def obtener_por_codigo(self, codigo: str) -> Optional[Producto]:
        """Obtiene un producto por su código único."""
        pass

    @abstractmethod
    def obtener_todos(self) -> list[Producto]:
        """Retorna todos los productos registrados."""
        pass

    @abstractmethod
    def actualizar(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        stock: int,
        categoria: Categoria,
    ) -> None:
        """Actualiza la información de un producto."""
        pass

    @abstractmethod
    def eliminar(self, codigo: str) -> None:
        """Elimina un producto por su código."""
        pass

    @abstractmethod
    def buscar_por_nombre(self, query: str) -> list[Producto]:
        """Busca productos por coincidencia en nombre o código."""
        pass

    @abstractmethod
    def filtrar_por_categoria(self, categoria: str) -> list[Producto]:
        """Filtra productos pertenecientes a una categoría."""
        pass

    @abstractmethod
    def contar(self) -> int:
        """Retorna la cantidad total de productos distintos."""
        pass

    @abstractmethod
    def total_unidades(self) -> int:
        """Retorna la cantidad acumulada de unidades en inventario."""
        pass

    @abstractmethod
    def valor_total(self) -> float:
        """Retorna el valor monetario global del inventario."""
        pass


# 2. IMPLEMENTACIÓN CONCRETA DEL REPOSITORIO DE PRODUCTOS

class ProductoRepositoryMemoria(IProductoRepository):
    """
    Implementación en memoria del repositorio de productos.
    Garantiza unicidad de códigos e indexación rápida.
    """

    def __init__(self) -> None:
        self.__codigos: set[str] = set()
        self.__productos_dict: dict[str, Producto] = {}
        self.__productos_list: list[Producto] = []

    def guardar(self, producto: Producto) -> None:
        codigo = producto.get_codigo()
        if codigo in self.__codigos:
            raise ValueError(f"El producto con código '{codigo}' ya está registrado.")
        self.__codigos.add(codigo)
        self.__productos_dict[codigo] = producto
        self.__productos_list.append(producto)

    def obtener_por_codigo(self, codigo: str) -> Optional[Producto]:
        return self.__productos_dict.get(codigo.strip().upper())

    def obtener_todos(self) -> list[Producto]:
        return list(self.__productos_list)

    def actualizar(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        stock: int,
        categoria: Categoria,
    ) -> None:
        producto = self.obtener_por_codigo(codigo)
        if not producto:
            raise KeyError(f"No existe ningún producto con el código '{codigo}'.")
        producto.set_nombre(nombre)
        producto.set_precio(precio)
        producto.set_stock(stock)
        producto.set_categoria(categoria)

    def eliminar(self, codigo: str) -> None:
        codigo_norm = codigo.strip().upper()
        producto = self.obtener_por_codigo(codigo_norm)
        if not producto:
            raise KeyError(f"No se puede eliminar: el código '{codigo_norm}' no existe.")
        self.__codigos.remove(codigo_norm)
        del self.__productos_dict[codigo_norm]
        self.__productos_list.remove(producto)

    def buscar_por_nombre(self, query: str) -> list[Producto]:
        texto = query.strip().lower()
        if not texto:
            return self.obtener_todos()
        return [
            p for p in self.__productos_list
            if texto in p.get_nombre().lower() or texto in p.get_codigo().lower()
        ]

    def filtrar_por_categoria(self, categoria: str) -> list[Producto]:
        cat_filtro = categoria.strip().lower()
        if not cat_filtro or cat_filtro == "todas":
            return self.obtener_todos()
        return [
            p for p in self.__productos_list
            if p.get_categoria().get_nombre().lower() == cat_filtro
        ]

    def contar(self) -> int:
        return len(self.__codigos)

    def total_unidades(self) -> int:
        return sum(p.get_stock() for p in self.__productos_list)

    def valor_total(self) -> float:
        return sum(p.calcular_valor_inventario() for p in self.__productos_list)


# 3. INTERFAZ ABSTRACTA DEL REPOSITORIO DE DESPACHOS

class IDespachoRepository(ABC):
    """
    Contrato abstracto que define las operaciones para la administración
    de órdenes de despacho utilizando una estructura lineal (Cola/Pila).
    """

    @abstractmethod
    def encolar_despacho(self, pedido: PedidoDespacho) -> None:
        """Agrega una solicitud a la cola de atención."""
        pass

    @abstractmethod
    def despachar_siguiente(self) -> PedidoDespacho:
        """Atiende y remueve la siguiente solicitud en orden FIFO."""
        pass

    @abstractmethod
    def consultar_proximo(self) -> PedidoDespacho:
        """Consulta la próxima solicitud en cola sin removerla."""
        pass

    @abstractmethod
    def listar_pendientes(self) -> list[PedidoDespacho]:
        """Retorna la lista de todas las órdenes en espera."""
        pass

    @abstractmethod
    def total_pendientes(self) -> int:
        """Retorna la cantidad de órdenes pendientes."""
        pass

    @abstractmethod
    def esta_vacio(self) -> bool:
        """Indica si no hay pedidos pendientes en la cola."""
        pass

    @abstractmethod
    def listar_historial(self) -> list[PedidoDespacho]:
        """Retorna el historial de despachos completados (LIFO)."""
        pass


# 4. IMPLEMENTACIÓN CONCRETA CON COLA LINEAL MANUAL

class DespachoColaRepository(IDespachoRepository):
    """
    Implementación del repositorio de despachos respaldado por la
    estructura lineal 'ColaLineal' manual (FIFO) y 'PilaLineal' (LIFO).
    
    Separa completamente el flujo logístico de la capa gráfica y conecta
    con el inventario para validar y descontar existencias físicas.
    """

    def __init__(
        self, producto_repo: Optional[IProductoRepository] = None
    ) -> None:
        """
        Inicializa el repositorio integrando la ColaLineal manual.
        
        Args:
            producto_repo: Instancia opcional del repositorio de productos
                           para validar y sincronizar el stock disponible.
        """
        # Estructura manual LINEAL COLA (FIFO) para solicitudes en espera
        self.__cola_pendientes: ColaLineal[PedidoDespacho] = ColaLineal()
        # Estructura manual LINEAL PILA (LIFO) para historial de despachos
        self.__historial_despachos: PilaLineal[PedidoDespacho] = PilaLineal()
        self.__producto_repo: Optional[IProductoRepository] = producto_repo

    def encolar_despacho(self, pedido: PedidoDespacho) -> None:
        """
        Registra una nueva orden en la cola FIFO.
        Si existe un repositorio de productos, valida que el producto exista
        y que haya stock suficiente para la solicitud.
        """
        if self.__producto_repo:
            producto = self.__producto_repo.obtener_por_codigo(pedido.get_codigo_producto())
            if not producto:
                raise KeyError(
                    f"No se puede encolar el pedido: El producto "
                    f"'{pedido.get_codigo_producto()}' no existe en el catálogo."
                )
            if producto.get_stock() < pedido.get_cantidad():
                raise ValueError(
                    f"Stock insuficiente en bodega para el producto '{producto.get_nombre()}'. "
                    f"Disponible: {producto.get_stock()} uds., "
                    f"Solicitado: {pedido.get_cantidad()} uds."
                )

        # Inserción en la cola manual O(1)
        self.__cola_pendientes.encolar(pedido)

    def despachar_siguiente(self) -> PedidoDespacho:
        """
        Extrae y procesa el pedido al frente de la cola (FIFO).
        Descuenta el stock físico del producto y guarda la orden en la pila de historial.
        
        Raises:
            ColaVaciaError: Si no hay despachos en espera.
            ValueError: Si el stock actual es insuficiente al momento del despacho.
        """
        if self.__cola_pendientes.esta_vacia():
            raise ColaVaciaError("No hay pedidos pendientes en la cola de despacho.")

        # Desencolar de la estructura lineal O(1)
        pedido = self.__cola_pendientes.desencolar()

        # Descontar stock del producto en el inventario si hay repositorio vinculado
        if self.__producto_repo:
            producto = self.__producto_repo.obtener_por_codigo(pedido.get_codigo_producto())
            if producto:
                if producto.get_stock() < pedido.get_cantidad():
                    # Si no hay suficiente stock ahora, se reencola o se lanza error
                    # Para consistencia transaccional:
                    raise ValueError(
                        f"Stock insuficiente al momento de despachar. "
                        f"Disponible: {producto.get_stock()}, "
                        f"Requerido: {pedido.get_cantidad()}."
                    )
                producto.disminuir_stock(pedido.get_cantidad())

        # Marcar estado como completado y apilar en el historial de auditoría
        pedido.marcar_despachado()
        self.__historial_despachos.apilar(pedido)

        return pedido

    def consultar_proximo(self) -> PedidoDespacho:
        """Consulta el siguiente pedido a despachar sin removerlo (Peek)."""
        return self.__cola_pendientes.ver_frente()

    def listar_pendientes(self) -> list[PedidoDespacho]:
        """Retorna todas las órdenes en espera en orden de turno."""
        return self.__cola_pendientes.a_lista()

    def total_pendientes(self) -> int:
        """Retorna el número de despachos pendientes."""
        return self.__cola_pendientes.tamano()

    def esta_vacio(self) -> bool:
        """Indica si la cola de despacho está vacía."""
        return self.__cola_pendientes.esta_vacia()

    def listar_historial(self) -> list[PedidoDespacho]:
        """Retorna las órdenes despachadas en orden cronológico inverso (LIFO)."""
        return self.__historial_despachos.a_lista()
