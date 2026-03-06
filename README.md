# 💾 Sistema de Inventarios con Python

Aplicación web moderna para la gestión de inventarios de productos tecnológicos, desarrollada con **Streamlit** y **SQLAlchemy**. Ofrece control completo de productos, seguimiento de movimientos, reportes detallados y visualización con imágenes.

![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.33.0-red.svg)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0.30-green.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.x-orange.svg)

![texto del vínculo](https://cdn.cpdonline.co.uk/wp-content/uploads/2023/04/28123407/Experienced-chef-de-partie-1200x350.jpg)

---

## 📋 Tabla de Contenidos

- [Características](#-características)
- [Capturas de Pantalla](#-capturas-de-pantalla)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Arquitectura](#-arquitectura)
- [Modelo de Datos](#-modelo-de-datos)
- [Migraciones](#-migraciones)
- [API Reference](#-api-reference)
- [Filtros Dinámicos](#-filtros-dinámicos)
- [Próximas Mejoras](#-próximas-mejoras)
- [Licencia](#-licencia)

---

## ✨ Características

### 📦 Control de Inventarios
- ✅ **ABM de Productos**: Altas, bajas y modificaciones
- ✅ **Búsqueda avanzada**: Filtrado por nombre y categoría
- ✅ **Vista dual**: Tabla tradicional o Tarjetas con imágenes
- ✅ **Categorías**: 9 categorías predefinidas (Laptops, Periféricos, Redes, etc.)
- ✅ **Proveedores**: Registro de proveedor por producto
- ✅ **SKU**: Código único de identificación
- ✅ **Stock mínimo configurable**: Alertas personaladas por producto
- ✅ **Imágenes de productos**: URLs de imágenes para cada producto
- ✅ **Exportar a CSV**: Descarga de inventario filtrado

### 📊 Informe de Inventario (Dashboard Interactivo)
- ✅ **4 Métricas en tiempo real**:
  - Total de productos
  - Valor total del inventario
  - Productos con stock bajo
  - Productos sin stock
- ✅ **Gráficos por categoría**: Distribución de valor y cantidad
- ✅ **Alertas visuales**: Colores según urgencia de reposición
- ✅ **Recomendaciones automáticas**: Sugerencias basadas en el estado del inventario
- ✅ **Filtros dinámicos**: El dashboard se actualiza según los filtros aplicados
- ✅ **Imágenes en tarjetas**: Vista visual con fotos de productos

### 📋 Gestión de Movimientos
- ✅ **Historial completo**: Registro de todas las entradas y salidas
- ✅ **Filtros avanzados**: Por fecha, tipo de movimiento y producto
- ✅ **Registro de entradas**: Compra, devolución, ajuste positivo
- ✅ **Registro de salidas**: Venta, merma, ajuste negativo
- ✅ **Validación de stock**: Previene salidas mayores al stock disponible
- ✅ **Motivo opcional**: Justificación de cada movimiento
- ✅ **Exportar movimientos**: Descarga de historial en CSV

### 💬 Asistente IA Inteligente (NUEVO)
- ✅ **Consultas en lenguaje natural**: Pregunta sobre stock, precios o estadísticas (Ej: "¿Qué laptops tienen poco stock?").
- ✅ **Agente autónomo**: Utiliza **OpenAI Function Calling** para consultar la base de datos en tiempo real.
- ✅ **Análisis de datos**: Capaz de calcular promedios, identificar tendencias y dar recomendaciones ejecutivas.
- ✅ **Historial de chat**: Mantiene el contexto de la conversación durante la sesión.

---

## 📸 Capturas de Pantalla

| Vista de Tarjetas | Dashboard con Filtros | Asistente IA |
|-------------------|----------------------|--------------|
| Productos con imágenes | Métricas filtradas dinámicamente | Chat interactivo con datos |

---

## 🛠️ Requisitos

| Dependencia | Versión |
|-------------|---------|
| Python | 3.10+ (compatible con 3.8+) |
| Streamlit | 1.33.0 |
| SQLAlchemy | 2.0.30 |
| OpenAI | 1.x (para el Asistente IA) |
| Python-Dotenv | 1.0.1 (para variables de entorno) |

---

## 📥 Instalación

### 1. Clonar o descargar el proyecto

```bash
cd "C:\Users\EdwinQuintero\Documents\Anaconda 3\Sistema_Inventarios"
```

### 2. Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con tu clave de API de OpenAI:

```env
OPENAI_API_KEY=tu_clave_aqui
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
# Instalación manual de dependencias de IA (si no están en requirements)
pip install openai python-dotenv
```

### 4. Inicializar la base de datos

```bash
# Ejecutar migración (agrega nuevas columnas y tabla movements)
python migrate.py

# Cargar datos de ejemplo (16 productos con imágenes)
python seed.py

# Actualizar productos con imágenes (si ya existe la BD)
python update_images.py
```

---

## 🚀 Uso

### Iniciar la aplicación

```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

### Primeros pasos

1. **Explorar productos**: Navega por la pestaña "Control de Inventarios"
2. **Cambiar vista**: Selecciona "🎴 Tarjetas" para ver imágenes
3. **Aplicar filtros**: Usa el sidebar para filtrar y aplica al Dashboard
4. **Ver dashboard**: Consulta métricas en "Informe de Inventario" (se actualiza con filtros)
5. **Registrar movimiento**: Usa la pestaña "Movimientos" para entradas/salidas

---

## 📁 Estructura del Proyecto

```
Sistema_Inventarios/
├── app.py                  # Interfaz principal (Streamlit)
├── ai_assistant.py         # Lógica del Asistente IA (OpenAI + Tools)
├── models.py               # Modelos ORM (SQLAlchemy)
├── db.py                   # Configuración de base de datos
├── repository.py           # Capa de acceso a datos (CRUD)
├── .env                    # Variables de entorno (API Keys)
├── seed.py                 # Script de datos iniciales
├── migrate.py              # Script de migración de BD
├── update_images.py        # Script para cargar imágenes
├── update_products.py      # Script para actualizar categorías/proveedores
├── requirements.txt        # Dependencias del proyecto
└── inventory.db            # Base de datos SQLite
```

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────┐
│                    Capa de Presentación                  │
│                      (app.py - Streamlit)                │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────┐  │
│  │   Control   │  │   Informe   │  │   Asistente IA  │  │
│  │  Inventarios│  │  (Dashboard)│  │   (OpenAI API)  │  │
│  └─────────────┘  └─────────────┘  └─────────────────┘  │
│         │                │                  │            │
│         └────────────────┼──────────────────┘            │
│                  Filtros Dinámicos                        │
│              (st.session_state global)                    │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Capa de Inteligencia                   │
│                    (ai_assistant.py)                     │
│  ┌──────────────┐  ┌──────────────┐  ┌───────────────┐  │
│  │ GPT-4o-mini  │  │ Function     │  │ Tool          │  │
│  │ (Razonamiento)│  │ Calling      │  │ Mapping       │  │
│  └──────────────┘  └──────────────┘  └───────────────┘  │
└─────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────┐
│                   Capa de Negocio                        │
│                   (repository.py)                        │
└─────────────────────────────────────────────────────────┘
```

---

## 🗄️ Modelo de Datos

### Tabla: `products`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | INTEGER | Clave primaria (autoincremental) |
| `name` | STRING | Nombre del producto |
| `price` | FLOAT | Precio unitario |
| `quantity` | INTEGER | Cantidad en stock |
| `category` | STRING | Categoría del producto |
| `supplier` | STRING | Proveedor del producto |
| `min_stock` | INTEGER | Stock mínimo para alertas |
| `sku` | STRING | Código SKU único |
| `image_url` | STRING | URL de la imagen del producto |

### Tabla: `movements`

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `id` | INTEGER | Clave primaria (autoincremental) |
| `product_id` | INTEGER | Clave foránea a products |
| `movement_type` | STRING | 'entrada' o 'salida' |
| `quantity` | INTEGER | Cantidad movida |
| `reason` | STRING | Motivo del movimiento |
| `created_at` | DATETIME | Fecha y hora del movimiento |

---

## 🔧 Migraciones

El script `migrate.py` actualiza la base de datos existente:

```bash
python migrate.py
```

**Acciones que realiza:**
- Agrega columnas: `category`, `supplier`, `min_stock`, `sku`, `image_url`
- Crea tabla `movements`
- Actualiza productos existentes con valores por defecto

### Scripts de Actualización

| Script | Propósito |
|--------|-----------|
| `update_products.py` | Asigna categorías y proveedores a productos existentes |
| `update_images.py` | Asigna URLs de imágenes a productos existentes |

---

## 📖 API Reference

### Productos

| Función | Descripción |
|---------|-------------|
| `add_product(...)` | Crear nuevo producto (con SKU e Imagen) |
| `remove_product(id)` | Eliminar producto por ID |
| `update_product(...)` | Actualizar cualquier campo del producto |
| `list_products()` | Listar todos los productos |
| `get_product_by_id(id)` | Obtener producto por ID |
| `get_categories()` | Listar categorías únicas |
| `search_products(term, cat)` | Buscar con filtros de nombre y categoría |

### Movimientos e IA

| Función | Descripción |
|---------|-------------|
| `register_movement(...)` | Registrar entrada/salida con validación |
| `get_movements(...)` | Historial filtrado por fecha y producto |
| `get_ai_response(msgs)` | Procesa mensajes con GPT-4o-mini y funciones |
| `get_inventory_stats()` | Estadísticas resumidas para Dashboard e IA |

---

## 🔗 Filtros Dinámicos e IA

### Cómo Funciona

1. **Filtros Globales**: Los filtros aplicados en "Control de Inventarios" se almacenan en `st.session_state`.
2. **Dashboard Reactivo**: El "Informe de Inventario" detecta estos filtros y recalcula métricas y gráficos automáticamente.
3. **Asistente IA**: El asistente tiene acceso a las mismas funciones de filtrado, permitiéndole "ver" lo mismo que el usuario o realizar búsquedas independientes.

### Flujo de Filtros

```
┌──────────────────────┐
│  Control de          │
│  Inventarios         │
│  ┌────────────────┐  │
│  │ Sidebar:       │  │
│  │ - Buscar       │  │
│  │ - Categoría    │  │
│  │ [Aplicar]      │  │
│  └────────────────┘  │
└──────────┬───────────┘
           │
           ▼
   st.session_state
   (filtros globales)
           │
           ▼
┌──────────┴───────────┐
│  Informe de          │
│  Inventario          │
│  ┌────────────────┐  │
│  │ Métricas       │  │
│  │ (filtradas)    │  │
│  │ Gráficos       │  │
│  │ (filtrados)    │  │
│  │ Tablas         │  │
│  │ (filtradas)    │  │
│  └────────────────┘  │
└──────────────────────┘
```

### Resetear Filtros

- **Desde Sidebar**: Botón "Limpiar filtros"
- **Desde Dashboard**: Botón "🔄 Ver todos los productos"

---

## 🔮 Próximas Mejoras

- [ ] **Usuarios y autenticación**: Login con roles (Admin/Viewer)
- [ ] **Exportar a Excel**: Con formato y múltiples hojas
- [ ] **Reportes en PDF**: Inventarios formateados para imprimir
- [ ] **Gráficos de tendencias**: Evolución de stock en el tiempo
- [ ] **Notificaciones por email**: Alertas de stock bajo
- [ ] **Código de barras**: Escaneo para búsqueda rápida
- [ ] **Backup automático**: Copias programadas de la base de datos
- [ ] **Subida de imágenes**: Cargar archivos locales en lugar de URLs

---

## 📄 Licencia

MIT © 2026

---

## 👨‍💻 Autor

Desarrollado como sistema de gestión de inventarios tecnológico.

---

## 🆘 Soporte

Para reportar errores o sugerencias, por favor crea un issue en el repositorio o contacta al equipo de desarrollo.

---

## 📝 Historial de Versiones

| Versión | Fecha | Mejoras |
|---------|-------|---------|
| 2.0 | 2026-02 | Filtros dinámicos, imágenes de productos, vista de tarjetas |
| 1.5 | 2026-02 | Historial de movimientos, categorías, proveedores |
| 1.0 | 2026-02 | Versión inicial con CRUD básico |
