# Sistema de Gestión de Bodega — Catálogo de Productos con Flet

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flet](https://img.shields.io/badge/GUI-Flet_1.0-02569B?style=for-the-badge&logo=flutter&logoColor=white)
![Pydantic](https://img.shields.io/badge/Pydantic-v2.13.4-E92063?style=for-the-badge&logo=pydantic&logoColor=white)
![Ruff](https://img.shields.io/badge/Linter-Ruff-D7FF64?style=for-the-badge&logo=ruff&logoColor=black)
![Actividad](https://img.shields.io/badge/POO-Semanas_5_y_6-1B365D?style=for-the-badge)

---

## 📌 Datos del Estudiante y Actividad

* **Estudiante:** Luis Alberto Villegas Merchan
* **Materia:** Programación Orientada a Objetos
* **Actividad:** Semanas 5 y 6 — Colecciones, Genéricos, Interfaz Gráfica (Flet) y Manejo de Eventos
* **Lenguaje:** Python 3.14
* **Framework Gráfico:** Flet (Flutter para Python)

---

## 📑 Tabla de Contenidos

1. [Descripción General](#-descripción-general)
2. [Semana 5: Colecciones y Operaciones CRUD](#-semana-5-colecciones-y-operaciones-crud)
3. [Semana 6: Interfaz Gráfica Flet y Manejo de Eventos](#-semana-6-interfaz-gráfica-flet-y-manejo-de-eventos)
4. [Estructura del Proyecto](#-estructura-del-proyecto)
5. [Instrucciones de Instalación y Ejecución](#-instrucciones-de-instalación-y-ejecución)
6. [Guía de Capturas para el Informe de Blackboard](#-guía-de-capturas-para-el-informe-de-blackboard)

---

## 📦 Descripción General

Este proyecto implementa un **Catálogo de Productos para la Gestión de Bodega e Inventario**, integrando de forma cohesiva los requerimientos de las Semanas 5 y 6:
* **Semana 5:** Almacenamiento y administración de información en memoria viva mediante el uso combinado de colecciones nativas de Python (`set`, `dict` y `list`) con operaciones CRUD completas y prevención de duplicados.
* **Semana 6:** Construcción de una interfaz gráfica de escritorio interactiva con **Flet**, manejo de eventos de usuario (`on_click`, `on_change`), validaciones y retroalimentación visual inmediata.

---

## 🧩 Semana 5: Colecciones y Operaciones CRUD

La clase `CatalogoProductos` en `modelo.py` administra el inventario utilizando tres colecciones especializadas:

| Colección | Propósito en el Catálogo | Justificación Técnica |
| :--- | :--- | :--- |
| **`set` (`__codigos_set`)** | **Evitar duplicados** y verificar existencia. | Comprobación de membresía en tiempo constante $O(1)$. Si un código ya existe, rechaza la inserción con un `ValueError`. |
| **`dict` (`__productos_dict`)** | **Búsqueda e indexación** directa por código (`codigo -> Producto`). | Acceso, consulta y actualización inmediata en tiempo $O(1)$ sin recorrer toda la colección. |
| **`list` (`__productos_list`)** | **Orden secuencial y filtrado**. | Mantiene el orden cronológico de registro, permitiendo listar, filtrar por categoría o buscar por coincidencia parcial de texto. |

### Operaciones CRUD Implementadas:
1. **[CREATE] `agregar_producto(producto)`:** Valida que el código no esté en el `set`, y luego lo inserta en `set`, `dict` y `list`.
2. **[READ] `buscar_por_codigo(codigo)`:** Consulta inmediata en el `dict`.
3. **[READ] `buscar_por_nombre(texto)` / `listar_por_categoria(cat)`:** Filtrado sobre la `list`.
4. **[UPDATE] `actualizar_producto(codigo, nombre, precio, stock, categoria)`:** Modifica los atributos encapsulados del producto seleccionado.
5. **[DELETE] `eliminar_producto(codigo)`:** Remueve el producto de forma sincronizada en `set`, `dict` y `list`.

---

## 🖥️ Semana 6: Interfaz Gráfica Flet y Manejo de Eventos

La interfaz desarrollada en `app.py` conecta los controles visuales con las colecciones del catálogo:

### 1. Controles y Formularios:
* **Campos de Entrada:** `TextField` para Código, Nombre, Precio y Stock, con iconos intuitivos.
* **Selector de Categoría:** `Dropdown` con opciones precargadas (*Accesorios, Electrónica, Herramientas, Redes, Almacenamiento*).
* **Tarjetas de Métricas:** Contadores superiores que calculan en tiempo real:
  * Total de productos registrados.
  * Total de unidades físicas en stock.
  * Valor monetario global del inventario ($\sum \text{precio} \times \text{stock}$).

### 2. Manejo de Eventos (`Event Handling`):
* **`on_click` en Botón "Guardar Producto":** Captura los datos del formulario, valida tipos y restricciones con **Pydantic**, inserta el producto en el catálogo y actualiza la tabla de datos.
* **`on_click` en Botón "Actualizar":** Modifica los valores del producto en edición.
* **`on_click` en Botón "Eliminar":** Elimina el producto tanto de la tabla visual como de las colecciones internas.
* **`on_click` en Botón "Limpiar":** Resetea los campos y restablece el estado de los botones.
* **`on_change` en Barra de Búsqueda y Filtro de Categoría:** Filtra la tabla en vivo conforme el usuario escribe o selecciona una categoría.
* **Selección de Fila en `DataTable`:** Al hacer clic en el botón de edición de una fila, carga automáticamente los datos del producto en el formulario para modificarlo o eliminarlo.

### 3. Validaciones y Mensajes al Usuario:
* **Notificaciones flotantes (`SnackBar`):**
  * 🟩 **Mensaje Verde (Éxito):** Confirma operaciones exitosas (ej. *"Producto PRD-007 agregado exitosamente"*).
  * 🟥 **Mensaje Rojo (Error):** Alerta de campos vacíos, precios negativos o intentos de ingresar códigos duplicados.

---

## 📁 Estructura del Proyecto

```text
poo semanas 5 y 6/
│
├── modelo.py              # Clases Categoria, Producto y CatalogoProductos (list, dict, set)
├── app.py                 # Interfaz gráfica moderna en Flet con manejo de eventos
├── main.py                # Punto de entrada (modo GUI y modo CLI para pruebas de consola)
├── requirements.txt       # Dependencias necesarias (flet, pydantic, ruff)
├── .gitignore             # Exclusión de temporales y cachés
└── README.md              # Documentación técnica completa
```

---

## 🚀 Instrucciones de Instalación y Ejecución

### 1. Instalar dependencias
Abre la terminal en la carpeta del proyecto y ejecuta:
```powershell
python -m pip install -r requirements.txt
```

### 2. Ejecutar la Aplicación Gráfica (Flet)
```powershell
python main.py
```
*(O también: `python app.py`)*

### 3. Ejecutar las Pruebas de Consola (Semana 5)
Si deseas ejecutar la demostración automatizada de las colecciones en terminal:
```powershell
python main.py --cli
```

---

## 📸 Guía de Capturas para el Informe de Blackboard

Para el documento PDF que debes entregar a tu profesor, se recomienda tomar las siguientes capturas de pantalla de la aplicación en funcionamiento:

1. **Pantalla Principal:** Mostrando la ventana con la tabla de productos precargada y las tarjetas de métricas.
2. **Registro de Producto Nuevo (CREATE):** Llenando el formulario con un nuevo producto y el mensaje verde `SnackBar` de éxito.
3. **Validación de Código Duplicado:** Intentando registrar un código que ya existe y mostrando la alerta roja del `set`.
4. **Búsqueda y Filtrado (READ):** Escribiendo en la barra de búsqueda o filtrando por categoría.
5. **Edición / Actualización (UPDATE):** Modificando el precio o stock de un producto y viendo el cambio en la tabla.
6. **Eliminación (DELETE):** Eliminando un producto del inventario.

---

## 👨‍💻 Autor

**Luis Alberto Villegas Merchan**  
Estudiante de Ingeniería de Software / Sistemas
