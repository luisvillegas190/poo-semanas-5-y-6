"""
modelo.py
=========

Modelo de dominio del Catálogo de Productos y Sistema de Gestión de Bodega.

Actividad: POO — Semanas 5 y 6 (Colecciones, Genéricos y Manejo de Eventos)
Autor: Luis Alberto Villegas Merchan

Este módulo implementa:
1. Modelos de validación con Pydantic (DatosCategoria, DatosProducto).
2. Clases de entidad encapsuladas (Categoria, Producto).
3. Gestor de catálogo utilizando Colecciones de Python:
   - set: Para garantizar la unicidad de códigos en tiempo O(1).
   - dict: Para indexación clave-valor (código -> Producto) y búsquedas rápidas.
   - list: Para mantener el orden de registro y permitir listados y filtros.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

# =====================================================================
# MODELOS DE VALIDACIÓN PYDANTIC
# =====================================================================

class DatosCategoria(BaseModel):
    """Valida los datos requeridos para una categoría."""

    codigo: str = Field(min_length=2, max_length=20)
    nombre: str = Field(min_length=2, max_length=80)


class DatosProducto(BaseModel):
    """Valida los datos requeridos para un producto."""

    codigo: str = Field(min_length=2, max_length=20)
    nombre: str = Field(min_length=2, max_length=100)
    precio: float = Field(gt=0)
    stock: int = Field(ge=0)


# =====================================================================
# CLASES DE DOMINIO (ENCAPSULACIÓN)
# =====================================================================

class Categoria:
    """Representa una categoría de productos en la bodega."""

    def __init__(self, codigo: str, nombre: str) -> None:
        datos = DatosCategoria(codigo=codigo, nombre=nombre)
        self.__codigo = datos.codigo.strip().upper()
        self.__nombre = datos.nombre.strip()

    def get_codigo(self) -> str:
        """Retorna el código de la categoría."""
        return self.__codigo

    def set_codigo(self, codigo: str) -> None:
        """Actualiza y valida el código de la categoría."""
        datos = DatosCategoria(codigo=codigo, nombre=self.__nombre)
        self.__codigo = datos.codigo.strip().upper()

    def get_nombre(self) -> str:
        """Retorna el nombre descriptivo de la categoría."""
        return self.__nombre

    def set_nombre(self, nombre: str) -> None:
        """Actualiza y valida el nombre de la categoría."""
        datos = DatosCategoria(codigo=self.__codigo, nombre=nombre)
        self.__nombre = datos.nombre.strip()

    def __str__(self) -> str:
        return self.__nombre

    def __repr__(self) -> str:
        return f"Categoria(codigo='{self.__codigo}', nombre='{self.__nombre}')"

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Categoria):
            return self.__codigo == other.get_codigo()
        return False

    def __hash__(self) -> int:
        return hash(self.__codigo)


class Producto:
    """
    Representa un producto almacenado en el inventario.
    Aplica encapsulación estricta mediante atributos privados (__).
    """

    def __init__(
        self,
        codigo: str,
        nombre: str,
        precio: float,
        stock: int,
        categoria: Categoria,
    ) -> None:
        datos = DatosProducto(
            codigo=codigo,
            nombre=nombre,
            precio=precio,
            stock=stock,
        )
        self.__codigo = datos.codigo.strip().upper()
        self.__nombre = datos.nombre.strip()
        self.__precio = datos.precio
        self.__stock = datos.stock
        self.__categoria = categoria

    def get_codigo(self) -> str:
        """Retorna el código único del producto."""
        return self.__codigo

    def get_nombre(self) -> str:
        """Retorna el nombre del producto."""
        return self.__nombre

    def set_nombre(self, nombre: str) -> None:
        """Actualiza y valida el nombre del producto."""
        datos = DatosProducto(
            codigo=self.__codigo,
            nombre=nombre,
            precio=self.__precio,
            stock=self.__stock,
        )
        self.__nombre = datos.nombre.strip()

    def get_precio(self) -> float:
        """Retorna el precio unitario del producto."""
        return self.__precio

    def set_precio(self, precio: float) -> None:
        """Actualiza y valida el precio unitario."""
        datos = DatosProducto(
            codigo=self.__codigo,
            nombre=self.__nombre,
            precio=precio,
            stock=self.__stock,
        )
        self.__precio = datos.precio

    def get_stock(self) -> int:
        """Retorna la cantidad en inventario."""
        return self.__stock

    def set_stock(self, stock: int) -> None:
        """Actualiza y valida la cantidad en inventario."""
        datos = DatosProducto(
            codigo=self.__codigo,
            nombre=self.__nombre,
            precio=self.__precio,
            stock=stock,
        )
        self.__stock = datos.stock

    def get_categoria(self) -> Categoria:
        """Retorna la categoría a la que pertenece."""
        return self.__categoria

    def set_categoria(self, categoria: Categoria) -> None:
        """Asigna una nueva categoría al producto."""
        self.__categoria = categoria

    def aumentar_stock(self, cantidad: int) -> None:
        """Aumenta el stock en una cantidad positiva."""
        if cantidad <= 0:
            raise ValueError("La cantidad a reabastecer debe ser positiva.")
        self.set_stock(self.__stock + cantidad)

    def disminuir_stock(self, cantidad: int) -> None:
        """Disminuye el stock verificando disponibilidad."""
        if cantidad <= 0:
            raise ValueError("La cantidad a descontar debe ser positiva.")
        if cantidad > self.__stock:
            raise ValueError(
                f"Stock insuficiente para el producto {self.__codigo}. "
                f"Disponible: {self.__stock}, Solicitado: {cantidad}."
            )
        self.set_stock(self.__stock - cantidad)

    def calcular_valor_inventario(self) -> float:
        """Calcula el valor monetario total en stock (precio * stock)."""
        return self.__precio * self.__stock

    def mostrar_informacion(self) -> str:
        """Devuelve un resumen del producto."""
        return (
            f"[{self.__codigo}] {self.__nombre} | "
            f"Categoría: {self.__categoria.get_nombre()} | "
            f"Precio: ${self.__precio:,.2f} | Stock: {self.__stock} uds."
        )

    def __str__(self) -> str:
        return self.mostrar_informacion()

    def __repr__(self) -> str:
        return (
            f"Producto(codigo='{self.__codigo}', nombre='{self.__nombre}', "
            f"precio={self.__precio}, stock={self.__stock})"
        )

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Producto):
            return self.__codigo == other.get_codigo()
        return False

    def __hash__(self) -> int:
        return hash(self.__codigo)


# =====================================================================
# SEMANA 5: GESTOR DEL CATÁLOGO MEDIANTE COLECCIONES (list, dict, set)
# =====================================================================

class CatalogoProductos:
    """
    Administra el catálogo de productos utilizando tres colecciones de Python:
    - set: Evita códigos duplicados y valida unicidad en O(1).
    - dict: Indexa productos por código (clave-valor) para búsquedas directas.
    - list: Mantiene el orden cronológico de registro para listados y filtros.

    Implementa operaciones CRUD completas (Crear, Consultar, Actualizar, Eliminar).
    """

    def __init__(self) -> None:
        self.__codigos_set: set[str] = set()
        self.__productos_dict: dict[str, Producto] = {}
        self.__productos_list: list[Producto] = []

    # ==================== OPERACIONES CRUD ====================

    def agregar_producto(self, producto: Producto) -> None:
        """
        [CREATE] Agrega un nuevo producto al catálogo.
        Verifica unicidad utilizando el set para evitar duplicados.
        """
        codigo = producto.get_codigo()

        # Validación de duplicados mediante 'set'
        if codigo in self.__codigos_set:
            raise ValueError(
                f"El código '{codigo}' ya existe en el catálogo. "
                "No se permiten productos duplicados."
            )

        # Inserción sincronizada en las tres colecciones
        self.__codigos_set.add(codigo)
        self.__productos_dict[codigo] = producto
        self.__productos_list.append(producto)

    def buscar_por_codigo(self, codigo: str) -> Producto | None:
        """
        [READ] Busca un producto por su código utilizando el dict O(1).
        """
        codigo_normalizado = codigo.strip().upper()
        return self.__productos_dict.get(codigo_normalizado)

    def buscar_por_nombre(self, texto_busqueda: str) -> list[Producto]:
        """
        [READ] Busca productos por coincidencia parcial de nombre en la list.
        """
        query = texto_busqueda.strip().lower()
        if not query:
            return self.listar_todos()

        return [
            p for p in self.__productos_list
            if query in p.get_nombre().lower() or query in p.get_codigo().lower()
        ]

    def listar_todos(self) -> list[Producto]:
        """
        [READ] Retorna una copia de la lista de todos los productos registrados.
        """
        return list(self.__productos_list)

    def listar_por_categoria(self, nombre_categoria: str) -> list[Producto]:
        """
        [READ] Filtra y lista productos pertenecientes a una categoría específica.
        """
        cat_query = nombre_categoria.strip().lower()
        if not cat_query or cat_query == "todas":
            return self.listar_todos()

        return [
            p for p in self.__productos_list
            if p.get_categoria().get_nombre().lower() == cat_query
        ]

    def actualizar_producto(
        self,
        codigo: str,
        nuevo_nombre: str,
        nuevo_precio: float,
        nuevo_stock: int,
        nueva_categoria: Categoria,
    ) -> None:
        """
        [UPDATE] Actualiza la información de un producto existente.
        """
        codigo_normalizado = codigo.strip().upper()
        producto = self.buscar_por_codigo(codigo_normalizado)

        if not producto:
            raise KeyError(
                f"No se encontró ningún producto con el código '{codigo_normalizado}'."
            )

        # Actualiza el objeto mediante sus métodos setters encapsulados
        producto.set_nombre(nuevo_nombre)
        producto.set_precio(nuevo_precio)
        producto.set_stock(nuevo_stock)
        producto.set_categoria(nueva_categoria)

    def eliminar_producto(self, codigo: str) -> None:
        """
        [DELETE] Elimina un producto del catálogo por su código.
        Sincroniza la remoción en set, dict y list.
        """
        codigo_normalizado = codigo.strip().upper()
        producto = self.buscar_por_codigo(codigo_normalizado)

        if not producto:
            raise KeyError(
                f"No se puede eliminar: el código '{codigo_normalizado}' no existe."
            )

        # Remoción en las tres colecciones
        self.__codigos_set.remove(codigo_normalizado)
        del self.__productos_dict[codigo_normalizado]
        self.__productos_list.remove(producto)

    # ==================== MÉTRICAS Y REPORTES ====================

    def total_productos(self) -> int:
        """Retorna la cantidad total de productos distintos registrados."""
        return len(self.__codigos_set)

    def total_unidades_stock(self) -> int:
        """Retorna la suma total de unidades físicas en inventario."""
        return sum(p.get_stock() for p in self.__productos_list)

    def valor_total_inventario(self) -> float:
        """Calcula el valor monetario global del inventario."""
        return sum(p.calcular_valor_inventario() for p in self.__productos_list)

    def cargar_datos_iniciales(self) -> None:
        """Carga un conjunto de categorías y productos iniciales de prueba."""
        cat_acc = Categoria("CAT-ACC", "Accesorios")
        cat_elec = Categoria("CAT-ELE", "Electrónica")
        cat_her = Categoria("CAT-HER", "Herramientas")
        cat_red = Categoria("CAT-RED", "Redes y Conectividad")

        productos_demo = [
            Producto("PRD-001", "Lector de Código de Barras Láser RF", 145.00, 25, cat_acc),
            Producto("PRD-002", "Terminal Portátil de Inventario Android", 380.00, 12, cat_elec),
            Producto("PRD-003", "Impresora Térmica de Etiquetas 4x6", 210.00, 18, cat_elec),
            Producto("PRD-004", "Bobina de Cable UTP Cat6 305m", 85.50, 30, cat_red),
            Producto("PRD-005", "Transpaleta Hidráulica Manual 2.5 Ton", 450.00, 6, cat_her),
            Producto("PRD-006", "Switch Gigabit Gestionable 24 Puertos", 175.00, 15, cat_red),
        ]

        for p in productos_demo:
            if p.get_codigo() not in self.__codigos_set:
                self.agregar_producto(p)
