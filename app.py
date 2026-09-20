"""
app.py
======

Interfaz Gráfica de Usuario (GUI) desarrollada con Flet para el Sistema de Bodega.

Actividad: POO — Semana 6: Interfaz gráfica y manejo de eventos
Autor: Luis Alberto Villegas Merchan

Características:
- Formulario de captura y edición de productos con validaciones.
- Manejo de eventos en botones (Crear, Consultar, Actualizar, Eliminar, Limpiar).
- Búsqueda y filtrado dinámico en tiempo real (evento on_change).
- Tabla de datos interactiva (DataTable) con selección de filas.
- Tarjetas de métricas del inventario actualizadas en tiempo real.
- Notificaciones emergentes (SnackBar) para retroalimentación al usuario.
"""

from __future__ import annotations

import flet as ft
from pydantic import ValidationError

from modelo import CatalogoProductos, Categoria, Producto


def crear_aplicacion(page: ft.Page) -> None:
    """Configura y ejecuta la interfaz gráfica de usuario en Flet."""

    # Configuración de la ventana principal
    page.title = "Sistema de Gestión de Bodega — Catálogo de Productos"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 20
    page.window.width = 1200
    page.window.height = 800
    page.window.min_width = 900
    page.window.min_height = 650

    # Instancia del catálogo con colecciones (Semana 5)
    catalogo = CatalogoProductos()
    catalogo.cargar_datos_iniciales()

    # Categorías disponibles
    categorias_disponibles = [
        Categoria("CAT-ACC", "Accesorios"),
        Categoria("CAT-ELE", "Electrónica"),
        Categoria("CAT-HER", "Herramientas"),
        Categoria("CAT-RED", "Redes y Conectividad"),
        Categoria("CAT-ALM", "Almacenamiento"),
    ]
    mapa_categorias = {cat.get_nombre(): cat for cat in categorias_disponibles}

    # =========================================================================
    # CONTROLES DE LA INTERFAZ
    # =========================================================================

    # 1. Campos del Formulario
    txt_codigo = ft.TextField(
        label="Código del Producto",
        prefix_icon=ft.Icons.QR_CODE_2,
        hint_text="Ej: PRD-007",
        border_radius=8,
        dense=True,
    )

    txt_nombre = ft.TextField(
        label="Nombre del Producto",
        prefix_icon=ft.Icons.INVENTORY_2_OUTLINED,
        hint_text="Ej: Lector Óptico de Código de Barras",
        border_radius=8,
        dense=True,
    )

    txt_precio = ft.TextField(
        label="Precio Unitario ($)",
        prefix_icon=ft.Icons.ATTACH_MONEY,
        hint_text="Ej: 125.50",
        border_radius=8,
        dense=True,
    )

    txt_stock = ft.TextField(
        label="Cantidad en Stock",
        prefix_icon=ft.Icons.NUMBERS,
        hint_text="Ej: 20",
        border_radius=8,
        dense=True,
    )

    dd_categoria = ft.Dropdown(
        label="Categoría",
        leading_icon=ft.Icons.CATEGORY_OUTLINED,
        options=[ft.dropdown.Option(cat.get_nombre()) for cat in categorias_disponibles],
        border_radius=8,
        dense=True,
        value="Accesorios",
    )

    # 2. Controles de Búsqueda y Filtro
    txt_buscar = ft.TextField(
        label="Buscar por código o nombre...",
        prefix_icon=ft.Icons.SEARCH,
        border_radius=8,
        dense=True,
        expand=True,
    )

    dd_filtro_cat = ft.Dropdown(
        label="Filtrar por Categoría",
        options=[ft.dropdown.Option("Todas")] + [
            ft.dropdown.Option(cat.get_nombre()) for cat in categorias_disponibles
        ],
        value="Todas",
        border_radius=8,
        dense=True,
        width=220,
    )

    # 3. Métricas del Inventario
    lbl_total_productos = ft.Text("0", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.BLUE_900)
    lbl_total_stock = ft.Text("0", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN_900)
    lbl_valor_inventario = ft.Text("$0.00", size=22, weight=ft.FontWeight.BOLD, color=ft.Colors.PURPLE_900)

    # 4. Tabla de Productos (DataTable)
    tabla_productos = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Código", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Nombre del Producto", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Categoría", weight=ft.FontWeight.BOLD)),
            ft.DataColumn(ft.Text("Precio", weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text("Stock", weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text("Valor Total", weight=ft.FontWeight.BOLD), numeric=True),
            ft.DataColumn(ft.Text("Acción", weight=ft.FontWeight.BOLD)),
        ],
        rows=[],
        border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
        border_radius=8,
        heading_row_color=ft.Colors.BLUE_50,
        show_bottom_border=True,
    )

    # =========================================================================
    # FUNCIONES AUXILIARES Y MANEJO DE EVENTOS
    # =========================================================================

    def notificar(mensaje: str, es_error: bool = False) -> None:
        """Muestra una notificación emergente (SnackBar) al usuario."""
        snack = ft.SnackBar(
            content=ft.Row([
                ft.Icon(
                    ft.Icons.ERROR_OUTLINE if es_error else ft.Icons.CHECK_CIRCLE_OUTLINE,
                    color=ft.Colors.WHITE,
                ),
                ft.Text(mensaje, color=ft.Colors.WHITE, weight=ft.FontWeight.W_500),
            ]),
            bgcolor=ft.Colors.RED_700 if es_error else ft.Colors.GREEN_700,
            duration=3500,
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()

    def actualizar_metricas() -> None:
        """Actualiza los valores de las tarjetas de métricas."""
        lbl_total_productos.value = str(catalogo.total_productos())
        lbl_total_stock.value = f"{catalogo.total_unidades_stock()} uds."
        lbl_valor_inventario.value = f"${catalogo.valor_total_inventario():,.2f}"

    def cargar_formulario_desde_producto(producto: Producto) -> None:
        """Carga los datos de un producto en el formulario para editar."""
        txt_codigo.value = producto.get_codigo()
        txt_codigo.read_only = True  # Bloqueamos el código al editar
        txt_nombre.value = producto.get_nombre()
        txt_precio.value = f"{producto.get_precio():.2f}"
        txt_stock.value = str(producto.get_stock())
        dd_categoria.value = producto.get_categoria().get_nombre()
        btn_agregar.disabled = True
        btn_actualizar.disabled = False
        btn_eliminar.disabled = False
        page.update()

    def recargar_tabla(lista_filtrada: list[Producto] | None = None) -> None:
        """Regenera las filas de la tabla según los datos del catálogo."""
        productos = lista_filtrada if lista_filtrada is not None else catalogo.listar_todos()
        filas = []

        for p in productos:
            codigo = p.get_codigo()
            # Capturador de evento para seleccionar fila
            def on_select_click(e, prod=p):
                cargar_formulario_desde_producto(prod)

            def on_delete_click(e, cod=codigo):
                ejecutar_eliminacion_directa(cod)

            filas.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(p.get_codigo(), weight=ft.FontWeight.W_600)),
                        ft.DataCell(ft.Text(p.get_nombre())),
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text(p.get_categoria().get_nombre(), size=12, color=ft.Colors.BLUE_900),
                                bgcolor=ft.Colors.BLUE_100,
                                border_radius=6,
                                padding=ft.Padding.symmetric(horizontal=8, vertical=2),
                            )
                        ),
                        ft.DataCell(ft.Text(f"${p.get_precio():,.2f}")),
                        ft.DataCell(
                            ft.Text(
                                f"{p.get_stock()} uds.",
                                color=ft.Colors.RED_700 if p.get_stock() <= 5 else ft.Colors.BLACK,
                                weight=ft.FontWeight.BOLD if p.get_stock() <= 5 else ft.FontWeight.NORMAL,
                            )
                        ),
                        ft.DataCell(ft.Text(f"${p.calcular_valor_inventario():,.2f}")),
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.Icons.EDIT_OUTLINED,
                                    icon_color=ft.Colors.BLUE_700,
                                    tooltip="Cargar en formulario para editar",
                                    on_click=on_select_click,
                                ),
                                ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE,
                                    icon_color=ft.Colors.RED_700,
                                    tooltip="Eliminar producto",
                                    on_click=on_delete_click,
                                ),
                            ], spacing=0)
                        ),
                    ],
                )
            )

        tabla_productos.rows = filas
        actualizar_metricas()
        page.update()

    def limpiar_formulario(e=None) -> None:
        """Limpia los campos del formulario y restablece los botones."""
        txt_codigo.value = ""
        txt_codigo.read_only = False
        txt_nombre.value = ""
        txt_precio.value = ""
        txt_stock.value = ""
        dd_categoria.value = "Accesorios"
        btn_agregar.disabled = False
        btn_actualizar.disabled = True
        btn_eliminar.disabled = True
        page.update()

    # ==================== MANEJADORES DE EVENTOS CRUD ====================

    def handle_agregar(e) -> None:
        """[CREATE] Evento on_click para registrar un nuevo producto."""
        codigo = txt_codigo.value.strip()
        nombre = txt_nombre.value.strip()
        precio_str = txt_precio.value.strip()
        stock_str = txt_stock.value.strip()
        cat_nombre = dd_categoria.value

        if not codigo or not nombre or not precio_str or not stock_str or not cat_nombre:
            notificar("Por favor, complete todos los campos del formulario.", es_error=True)
            return

        try:
            precio = float(precio_str)
            stock = int(stock_str)
            categoria_obj = mapa_categorias[cat_nombre]

            # Instanciación con validación Pydantic interna
            nuevo_prod = Producto(
                codigo=codigo,
                nombre=nombre,
                precio=precio,
                stock=stock,
                categoria=categoria_obj,
            )

            # Inserción en catálogo (valida unicidad con set)
            catalogo.agregar_producto(nuevo_prod)
            notificar(f"✅ Producto '{codigo}' ({nombre}) agregado exitosamente.")
            limpiar_formulario()
            recargar_tabla()

        except ValidationError as err:
            primer_error = err.errors()[0]["msg"]
            notificar(f"Error de validación: {primer_error}", es_error=True)
        except (ValueError, KeyError, TypeError) as err:
            notificar(str(err), es_error=True)

    def handle_actualizar(e) -> None:
        """[UPDATE] Evento on_click para modificar el producto seleccionado."""
        codigo = txt_codigo.value.strip()
        nombre = txt_nombre.value.strip()
        precio_str = txt_precio.value.strip()
        stock_str = txt_stock.value.strip()
        cat_nombre = dd_categoria.value

        if not codigo or not nombre or not precio_str or not stock_str:
            notificar("Debe llenar todos los campos para actualizar.", es_error=True)
            return

        try:
            precio = float(precio_str)
            stock = int(stock_str)
            categoria_obj = mapa_categorias[cat_nombre]

            catalogo.actualizar_producto(
                codigo=codigo,
                nuevo_nombre=nombre,
                nuevo_precio=precio,
                nuevo_stock=stock,
                nueva_categoria=categoria_obj,
            )

            notificar(f"✏️ Producto '{codigo}' actualizado correctamente.")
            limpiar_formulario()
            recargar_tabla()

        except (ValidationError, ValueError, KeyError, TypeError) as err:
            notificar(f"Error al actualizar: {err}", es_error=True)

    def ejecutar_eliminacion_directa(codigo: str) -> None:
        """[DELETE] Elimina un producto por su código."""
        try:
            catalogo.eliminar_producto(codigo)
            notificar(f"🗑️ Producto '{codigo}' eliminado del catálogo.")
            limpiar_formulario()
            recargar_tabla()
        except KeyError as err:
            notificar(str(err), es_error=True)

    def handle_eliminar(e) -> None:
        """[DELETE] Evento on_click para eliminar el producto en formulario."""
        codigo = txt_codigo.value.strip()
        if not codigo:
            notificar("Seleccione un producto para eliminar.", es_error=True)
            return
        ejecutar_eliminacion_directa(codigo)

    def handle_buscar_o_filtrar(e) -> None:
        """[READ] Evento on_change en búsqueda o cambio de categoría."""
        query = txt_buscar.value.strip()
        categoria_sel = dd_filtro_cat.value

        # Paso 1: Filtro por búsqueda de texto (nombre o código)
        resultados = catalogo.buscar_por_nombre(query)

        # Paso 2: Filtro adicional por categoría si aplica
        if categoria_sel and categoria_sel != "Todas":
            resultados = [
                p for p in resultados
                if p.get_categoria().get_nombre().lower() == categoria_sel.lower()
            ]

        recargar_tabla(resultados)

    # Conectar eventos de búsqueda
    txt_buscar.on_change = handle_buscar_o_filtrar
    dd_filtro_cat.on_change = handle_buscar_o_filtrar

    # 4. Botones de Acción del Formulario
    btn_agregar = ft.FilledButton(
        "Guardar Producto",
        icon=ft.Icons.ADD_CIRCLE_OUTLINE,
        bgcolor=ft.Colors.BLUE_700,
        color=ft.Colors.WHITE,
        height=42,
        on_click=handle_agregar,
    )

    btn_actualizar = ft.FilledButton(
        "Actualizar",
        icon=ft.Icons.EDIT_NOTE,
        bgcolor=ft.Colors.AMBER_800,
        color=ft.Colors.WHITE,
        height=42,
        disabled=True,
        on_click=handle_actualizar,
    )

    btn_eliminar = ft.FilledButton(
        "Eliminar",
        icon=ft.Icons.DELETE_FOREVER,
        bgcolor=ft.Colors.RED_700,
        color=ft.Colors.WHITE,
        height=42,
        disabled=True,
        on_click=handle_eliminar,
    )

    btn_limpiar = ft.OutlinedButton(
        "Limpiar",
        icon=ft.Icons.CLEANING_SERVICES_OUTLINED,
        height=42,
        on_click=limpiar_formulario,
    )

    def toggle_theme(e):
        page.theme_mode = (
            ft.ThemeMode.DARK if page.theme_mode == ft.ThemeMode.LIGHT else ft.ThemeMode.LIGHT
        )
        theme_btn.icon = (
            ft.Icons.LIGHT_MODE if page.theme_mode == ft.ThemeMode.DARK else ft.Icons.DARK_MODE
        )
        page.update()

    theme_btn = ft.IconButton(
        icon=ft.Icons.DARK_MODE,
        tooltip="Cambiar Modo Claro / Oscuro",
        on_click=toggle_theme,
    )

    # =========================================================================
    # ESTRUCTURA VISUAL (LAYOUT)
    # =========================================================================

    # Encabezado
    header = ft.Container(
        content=ft.Row([
            ft.Row([
                ft.Icon(ft.Icons.WAREHOUSE, size=38, color=ft.Colors.BLUE_700),
                ft.Column([
                    ft.Text(
                        "Sistema de Gestión de Bodega — Catálogo de Productos",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Text(
                        "POO Semanas 5 y 6 (Colecciones list/dict/set, GUI en Flet y Manejo de Eventos) | Estudiante: Luis Alberto Villegas Merchan",
                        size=12,
                        color=ft.Colors.GREY_700,
                    ),
                ], spacing=2),
            ]),
            theme_btn,
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        padding=ft.Padding.only(bottom=10),
    )

    # Tarjetas de Métricas
    metricas_cards = ft.Row([
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.INVENTORY, size=32, color=ft.Colors.BLUE_700),
                ft.Column([
                    ft.Text("Productos Distintos (set/dict)", size=12, color=ft.Colors.GREY_700),
                    lbl_total_productos,
                ], spacing=1),
            ]),
            bgcolor=ft.Colors.BLUE_50,
            border=ft.Border.all(1, ft.Colors.BLUE_200),
            border_radius=10,
            padding=15,
            expand=True,
        ),
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.STORAGE, size=32, color=ft.Colors.GREEN_700),
                ft.Column([
                    ft.Text("Total Unidades en Stock", size=12, color=ft.Colors.GREY_700),
                    lbl_total_stock,
                ], spacing=1),
            ]),
            bgcolor=ft.Colors.GREEN_50,
            border=ft.Border.all(1, ft.Colors.GREEN_200),
            border_radius=10,
            padding=15,
            expand=True,
        ),
        ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.ACCOUNT_BALANCE_WALLET, size=32, color=ft.Colors.PURPLE_700),
                ft.Column([
                    ft.Text("Valor Total del Inventario", size=12, color=ft.Colors.GREY_700),
                    lbl_valor_inventario,
                ], spacing=1),
            ]),
            bgcolor=ft.Colors.PURPLE_50,
            border=ft.Border.all(1, ft.Colors.PURPLE_200),
            border_radius=10,
            padding=15,
            expand=True,
        ),
    ], spacing=15)

    # Panel Izquierdo: Formulario de Registro / Edición
    card_formulario = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.APP_REGISTRATION, color=ft.Colors.BLUE_700),
                ft.Text("Formulario de Producto", size=16, weight=ft.FontWeight.BOLD),
            ]),
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            txt_codigo,
            txt_nombre,
            ft.Row([txt_precio, txt_stock], spacing=10),
            dd_categoria,
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            ft.Column([
                ft.Row([btn_agregar, btn_limpiar], spacing=10),
                ft.Row([btn_actualizar, btn_eliminar], spacing=10),
            ], spacing=10),
        ], spacing=12),
        width=380,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
        border_radius=12,
        padding=18,
    )

    # Panel Derecho: Búsqueda, Filtros y Tabla
    card_catalogo = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.LIST_ALT, color=ft.Colors.BLUE_700),
                ft.Text("Catálogo de Productos en Inventario", size=16, weight=ft.FontWeight.BOLD),
            ]),
            ft.Divider(height=1, color=ft.Colors.GREY_300),
            ft.Row([txt_buscar, dd_filtro_cat], spacing=10),
            ft.Container(
                content=ft.ListView(
                    controls=[tabla_productos],
                    expand=True,
                ),
                expand=True,
                border=ft.Border.all(1, ft.Colors.GREY_200),
                border_radius=8,
                padding=5,
            ),
        ], spacing=12),
        expand=True,
        bgcolor=ft.Colors.WHITE,
        border=ft.Border.all(1, ft.Colors.BLUE_GREY_100),
        border_radius=12,
        padding=18,
    )

    # Armado final del contenido de la página
    cuerpo_principal = ft.Row(
        [card_formulario, card_catalogo],
        alignment=ft.MainAxisAlignment.START,
        vertical_alignment=ft.CrossAxisAlignment.START,
        expand=True,
        spacing=15,
    )

    page.add(
        ft.Column(
            [header, metricas_cards, ft.Container(height=5), cuerpo_principal],
            expand=True,
            spacing=10,
        )
    )

    # Carga inicial de datos en la tabla
    recargar_tabla()


def main():
    """Ejecuta la aplicación de escritorio Flet."""
    if hasattr(ft, "run"):
        ft.run(crear_aplicacion)
    else:
        ft.app(target=crear_aplicacion)


if __name__ == "__main__":
    main()
