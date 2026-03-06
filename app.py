import streamlit as st
import ai_assistant
from repository import (
    list_products,
    add_product,
    update_product,
    remove_product,
    get_inventory_stats,
    get_low_stock_products,
    get_categories,
    search_products,
    get_product_by_id,
    get_products_by_category_value,
    register_movement,
    get_movements,
    get_movement_stats,
    export_to_dict,
)

st.set_page_config(page_title="Inventario Tecnológico", layout="wide")

st.title("💾 Inventario Tecnológico")

# --- Inicializar estado de sesión para filtros globales ---
if "filtro_categoria" not in st.session_state:
    st.session_state.filtro_categoria = "Todas"
if "filtro_busqueda" not in st.session_state:
    st.session_state.filtro_busqueda = ""
if "filtro_activo" not in st.session_state:
    st.session_state.filtro_activo = False

# --- Inicializar estado para el Chat IA ---
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system", 
            "content": "Eres un asistente ejecutivo de inventarios. Tu objetivo es dar respuestas directas, precisas y muy concisas. NO desgloses cálculos matemáticos paso a paso ni expliques el procedimiento a menos que el usuario lo solicite. Si te piden un promedio o un total, da el resultado final de inmediato."
        },
        {"role": "assistant", "content": "¡Hola! Soy tu asistente de inventario. ¿Qué dato necesitas consultar?"}
    ]

# --- Funciones para manejar filtros ---
def aplicar_filtro(categoria, busqueda):
    st.session_state.filtro_categoria = categoria
    st.session_state.filtro_busqueda = busqueda
    st.session_state.filtro_activo = True

def resetear_filtros():
    st.session_state.filtro_categoria = "Todas"
    st.session_state.filtro_busqueda = ""
    st.session_state.filtro_activo = False

def obtener_productos_filtrados():
    if st.session_state.filtro_activo:
        cat = st.session_state.filtro_categoria if st.session_state.filtro_categoria != "Todas" else None
        return search_products(st.session_state.filtro_busqueda, cat)
    return list_products()

# --- Navegación por pestañas ---
tab_control, tab_informe, tab_movimientos, tab_chat = st.tabs([
    "📦 Control de Inventarios",
    "📊 Informe de Inventario",
    "📋 Movimientos",
    "💬 Asistente IA"
])

# =============================================================================
# PESTAÑA 1: CONTROL DE INVENTARIOS
# =============================================================================
with tab_control:
    st.header("Gestión de Productos")

    # --- Sidebar con filtros y acciones ---
    with st.sidebar:
        st.subheader("🔍 Filtros y Acciones")

        # Mostrar estado de filtros activos
        if st.session_state.filtro_activo:
            st.info(f"📌 Filtros activos:\n- Categoría: {st.session_state.filtro_categoria}\n- Búsqueda: '{st.session_state.filtro_busqueda}'")
            if st.button("Limpiar filtros", use_container_width=True):
                resetear_filtros()
                st.rerun()
            st.divider()

        if st.button("Actualizar lista", use_container_width=True):
            st.rerun()

        st.divider()

        # Buscar producto
        search_term = st.text_input("Buscar por nombre", placeholder="Ej: Laptop",
                                     value=st.session_state.filtro_busqueda, key="search_input")

        # Filtrar por categoría
        categories = get_categories()
        selected_category = st.selectbox(
            "Filtrar por categoría",
            options=["Todas"] + categories,
            index=0 if st.session_state.filtro_categoria == "Todas" else (categories.index(st.session_state.filtro_categoria) + 1 if st.session_state.filtro_categoria in categories else 0),
            key="category_select"
        )

        # Botón para aplicar filtros
        if st.button("Aplicar filtros al Dashboard", use_container_width=True, type="primary"):
            aplicar_filtro(selected_category, search_term)
            st.success("✅ Filtros aplicados al Dashboard")
            st.info("💡 Ve a la pestaña 'Informe de Inventario' para ver los resultados filtrados")

        st.divider()

        # Exportar CSV
        if search_term or selected_category != "Todas":
            products_for_export = search_products(search_term, selected_category if selected_category != "Todas" else None)
        else:
            products_for_export = list_products()

        if products_for_export:
            csv_data = "id,Nombre,Precio,Cantidad,Categoría,Proveedor,SKU,Stock Mínimo\n" + "\n".join(
                f"{p['id']},{p['name']},{p['price']},{p['quantity']},{p['category']},{p['supplier']},{p['sku']},{p['min_stock']}"
                for p in products_for_export
            )
            st.download_button(
                "📥 Exportar CSV",
                csv_data,
                "inventario.csv",
                mime="text/csv",
                use_container_width=True,
            )

    # --- Obtener productos filtrados (usa filtros locales, no globales) ---
    if search_term or (selected_category and selected_category != "Todas"):
        filtered = search_products(
            search_term,
            selected_category if selected_category != "Todas" else None
        )
    else:
        filtered = list_products()

    # --- Selector de vista: Tabla o Tarjetas ---
    st.subheader("📋 Lista de Productos")

    view_mode = st.radio(
        "Vista:",
        options=["📊 Tabla", "🎴 Tarjetas"],
        horizontal=True,
        label_visibility="collapsed"
    )

    # --- Vista de Tabla ---
    if view_mode == "📊 Tabla":
        if filtered:
            df = st.dataframe(
                {
                    "ID": [p["id"] for p in filtered],
                    "Nombre": [p["name"] for p in filtered],
                    "Categoría": [p["category"] or "General" for p in filtered],
                    "Precio": [f"${p['price']:.2f}" for p in filtered],
                    "Cantidad": [p["quantity"] for p in filtered],
                    "Proveedor": [p["supplier"] or "-" for p in filtered],
                    "SKU": [p["sku"] or "-" for p in filtered],
                },
                hide_index=True,
                height=400,
                use_container_width=True,
            )
        else:
            st.warning("⚠️ No se encontraron productos con esos filtros.")

    # --- Vista de Tarjetas con Imágenes ---
    elif view_mode == "🎴 Tarjetas":
        if filtered:
            # Mostrar productos en grid de 3 columnas
            cols = st.columns(3)
            for idx, product in enumerate(filtered):
                with cols[idx % 3]:
                    with st.container():
                        # Imagen del producto
                        if product.get("image_url"):
                            st.image(product["image_url"], use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/400x300?text=Sin+Imagen", use_container_width=True)

                        # Información del producto
                        st.subheader(product["name"])
                        st.caption(f"{product['category'] or 'General'} | SKU: {product['sku'] or 'N/A'}")
                        st.markdown(f"**${product['price']:.2f}**")

                        # Stock con indicador de color
                        if product["quantity"] == 0:
                            st.error(f"🔴 Sin stock")
                        elif product["quantity"] < (product["min_stock"] or 10):
                            st.warning(f"⚠️ Stock bajo: {product['quantity']} un.")
                        else:
                            st.success(f"✅ En stock: {product['quantity']} un.")

                        # Proveedor
                        if product.get("supplier"):
                            st.caption(f"🏭 {product['supplier']}")

                        st.divider()

            st.info(f"📦 Mostrando {len(filtered)} producto(s)")
        else:
            st.warning("⚠️ No se encontraron productos con esos filtros.")

    st.divider()

    # --- Operaciones ---
    st.subheader("⚙️ Operaciones")

    col1, col2, col3 = st.columns(3)

    with col1:
        with st.expander("➕ Agregar producto", expanded=False):
            name = st.text_input("Nombre", key="add_name")
            category = st.selectbox(
                "Categoría",
                options=["General", "Laptops", "PC Escritorio", "Periféricos", "Componentes", "Almacenamiento", "Redes", "Software", "Accesorios"],
                key="add_category"
            )
            price = st.number_input("Precio", min_value=0.0, step=0.01, key="add_price")
            quantity = st.number_input("Cantidad", min_value=0, step=1, key="add_qty")
            supplier = st.text_input("Proveedor", key="add_supplier")
            sku = st.text_input("SKU (opcional)", key="add_sku")
            min_stock = st.number_input("Stock mínimo alerta", min_value=1, step=1, value=10, key="add_min_stock")
            image_url = st.text_input("URL de imagen (opcional)", placeholder="https://...", key="add_image")

            if st.button("Agregar", use_container_width=True, key="btn_add"):
                if name.strip() and price is not None and quantity is not None:
                    add_product(
                        name=name,
                        price=price,
                        quantity=quantity,
                        category=category,
                        supplier=supplier,
                        min_stock=min_stock,
                        sku=sku,
                        image_url=image_url if image_url.strip() else None,
                    )
                    st.success(f"✅ Producto '{name}' añadido.")
                    st.rerun()
                else:
                    st.error("❌ Completa todos los campos obligatorios.")

    with col2:
        with st.expander("✏️ Actualizar producto", expanded=False):
            pid = st.number_input("ID del producto", min_value=1, step=1, key="upd_id")
            new_price = st.number_input("Nuevo precio", min_value=0.0, step=0.01, value=None, key="upd_price")
            new_qty = st.number_input("Nueva cantidad", min_value=0, step=1, value=None, key="upd_qty")
            new_category = st.selectbox(
                "Nueva categoría",
                options=["Sin cambio"] + ["General", "Laptops", "PC Escritorio", "Periféricos", "Componentes", "Almacenamiento", "Redes", "Software", "Accesorios"],
                key="upd_category"
            )
            new_supplier = st.text_input("Nuevo proveedor", key="upd_supplier")
            new_min_stock = st.number_input("Nuevo stock mínimo", min_value=1, step=1, value=None, key="upd_min_stock")
            new_sku = st.text_input("Nuevo SKU", key="upd_sku")
            new_image_url = st.text_input("Nueva URL de imagen (opcional)", placeholder="https://...", key="upd_image")

            if st.button("Actualizar", use_container_width=True, key="btn_update"):
                has_changes = any([
                    new_price is not None,
                    new_qty is not None,
                    new_category != "Sin cambio",
                    new_supplier.strip(),
                    new_min_stock is not None,
                    new_sku.strip(),
                    new_image_url.strip(),
                ])
                if has_changes:
                    res = update_product(
                        pid,
                        price=new_price if new_price is not None else None,
                        quantity=new_qty if new_qty is not None else None,
                        category=new_category if new_category != "Sin cambio" else None,
                        supplier=new_supplier if new_supplier.strip() else None,
                        min_stock=new_min_stock,
                        sku=new_sku if new_sku.strip() else None,
                        image_url=new_image_url if new_image_url.strip() else None,
                    )
                    if res:
                        st.success(f"✅ Producto {pid} actualizado.")
                        st.rerun()
                    else:
                        st.error(f"❌ ID {pid} no encontrado.")
                else:
                    st.warning("⚠️ Ingresa al menos un valor nuevo.")

    with col3:
        with st.expander("🗑️ Eliminar producto", expanded=False):
            del_id = st.number_input("ID a borrar", min_value=1, step=1, key="del_id")
            if st.button("Eliminar", use_container_width=True, key="btn_delete"):
                if remove_product(del_id):
                    st.success(f"✅ Producto {del_id} eliminado.")
                    st.rerun()
                else:
                    st.warning(f"⚠️ No existe producto con ID {del_id}.")

# =============================================================================
# PESTAÑA 2: INFORME DE INVENTARIO
# =============================================================================
with tab_informe:
    st.header("📊 Dashboard de Inventario")

    # --- Mostrar filtros activos ---
    if st.session_state.filtro_activo:
        st.info(f"📌 Viendo datos filtrados por: Categoría='{st.session_state.filtro_categoria}', Búsqueda='{st.session_state.filtro_busqueda}'")

        # Obtener productos filtrados para el dashboard
        productos_dashboard = obtener_productos_filtrados()

        # Calcular estadísticas filtradas
        from sqlalchemy import func
        from db import get_session
        from models import Product

        # Estadísticas personalizadas para productos filtrados
        total_products = len(productos_dashboard)
        total_value = sum(p["price"] * p["quantity"] for p in productos_dashboard)
        low_stock_products = [p for p in productos_dashboard if p["quantity"] < (p["min_stock"] or 10)]
        out_of_stock = [p for p in productos_dashboard if p["quantity"] == 0]
        avg_price = sum(p["price"] for p in productos_dashboard) / total_products if total_products > 0 else 0

        # Valor por categoría (filtrado)
        category_data = {}
        for p in productos_dashboard:
            cat = p["category"] or "General"
            if cat not in category_data:
                category_data[cat] = {"count": 0, "value": 0}
            category_data[cat]["count"] += 1
            category_data[cat]["value"] += p["price"] * p["quantity"]

        category_value = [{"category": cat, "count": data["count"], "value": round(data["value"], 2)}
                         for cat, data in category_data.items()]

        stats = {
            "total_products": total_products,
            "total_value": round(total_value, 2),
            "low_stock_count": len(low_stock_products),
            "out_of_stock_count": len(out_of_stock),
            "avg_price": round(avg_price, 2),
        }

        # Botón para resetear filtros desde el dashboard
        if st.button("🔄 Ver todos los productos", type="primary"):
            resetear_filtros()
            st.rerun()
    else:
        # Sin filtros - mostrar todos los datos
        productos_dashboard = list_products()
        stats = get_inventory_stats()
        low_stock_products = get_low_stock_products()
        category_value = get_products_by_category_value()

    # --- Métricas principales ---
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📦 Total Productos",
            value=stats["total_products"],
            help="Cantidad de productos registrados"
        )

    with col2:
        st.metric(
            label="💰 Valor del Inventario",
            value=f"${stats['total_value']:,.2f}",
            help="Suma total de precio × cantidad"
        )

    with col3:
        st.metric(
            label="⚠️ Stock Bajo",
            value=stats["low_stock_count"],
            help="Productos por debajo del stock mínimo",
            delta="-" if stats["low_stock_count"] == 0 else f"{stats['low_stock_count']} requieren atención",
            delta_color="inverse"
        )

    with col4:
        st.metric(
            label="🔴 Sin Stock",
            value=stats["out_of_stock_count"],
            help="Productos con 0 unidades",
            delta="Crítico" if stats["out_of_stock_count"] > 0 else "OK",
            delta_color="inverse"
        )

    st.divider()

    # --- Gráficos ---
    st.subheader("📈 Análisis por Categoría")

    if category_value:
        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            # Gráfico de barras - Valor por categoría
            chart_data = {cat["category"]: cat["value"] for cat in category_value}
            st.bar_chart(chart_data, y_label="Valor ($)")

        with col_chart2:
            # Gráfico de barras horizontal - Cantidad de productos por categoría
            pie_data = {cat["category"]: cat["count"] for cat in category_value}
            st.bar_chart(pie_data, y_label="Cantidad de productos")

        # Tabla de resumen por categoría
        st.dataframe(
            {
                "Categoría": [cat["category"] for cat in category_value],
                "Productos": [cat["count"] for cat in category_value],
                "Valor Total": [f"${cat['value']:,.2f}" for cat in category_value],
            },
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("ℹ️ No hay datos para mostrar gráficos.")

    st.divider()

    # --- Alertas de stock bajo ---
    st.subheader("🚨 Alertas de Stock Bajo")

    if low_stock_products:
        low_stock_data = {
            "ID": [p["id"] for p in low_stock_products],
            "Nombre": [p["name"] for p in low_stock_products],
            "Categoría": [p["category"] or "General" for p in low_stock_products],
            "Stock Actual": [p["quantity"] for p in low_stock_products],
            "Stock Mínimo": [p["min_stock"] for p in low_stock_products],
            "Proveedor": [p["supplier"] or "-" for p in low_stock_products],
        }

        df_low = st.dataframe(
            low_stock_data,
            hide_index=True,
            use_container_width=True,
            height=300,
        )

        st.warning(f"⚠️ Hay **{len(low_stock_products)} productos** que requieren reposición.")
    else:
        st.success("✅ Todos los productos tienen stock suficiente.")

    st.divider()

    # --- Lista completa de productos (filtrados) ---
    st.subheader("📋 Inventario Completo")

    if productos_dashboard:
        df_all = st.dataframe(
            {
                "ID": [p["id"] for p in productos_dashboard],
                "Nombre": [p["name"] for p in productos_dashboard],
                "Categoría": [p["category"] or "General" for p in productos_dashboard],
                "Precio": [f"${p['price']:.2f}" for p in productos_dashboard],
                "Cantidad": [p["quantity"] for p in productos_dashboard],
                "Valor Total": [f"${p['price'] * p['quantity']:,.2f}" for p in productos_dashboard],
                "Proveedor": [p["supplier"] or "-" for p in productos_dashboard],
            },
            hide_index=True,
            use_container_width=True,
            height=400,
        )
    else:
        st.info("ℹ️ No hay productos registrados en el inventario.")

    st.divider()

    # --- Recomendaciones ---
    st.subheader("💡 Recomendaciones")

    if st.session_state.filtro_activo:
        st.caption(f"📊 Las recomendaciones se basan en los {len(productos_dashboard)} productos filtrados.")

    if stats["out_of_stock_count"] > 0:
        st.error(f"🔴 **Acción inmediata:** Hay {stats['out_of_stock_count']} productos sin stock. ¡Reponer urgentemente!")

    if stats["low_stock_count"] > 0:
        st.warning(f"🟠 **Atención:** {stats['low_stock_count']} productos están por debajo del stock mínimo.")

    if stats["total_products"] == 0:
        if st.session_state.filtro_activo:
            st.info("ℹ️ No hay productos con los filtros seleccionados. Prueba limpiando los filtros.")
        else:
            st.info("ℹ️ El inventario está vacío. Comienza agregando productos en la pestaña 'Control de Inventarios'.")

    if stats["low_stock_count"] == 0 and stats["out_of_stock_count"] == 0 and stats["total_products"] > 0:
        st.success("✅ El inventario está en óptimas condiciones. Todos los productos tienen stock adecuado.")

# =============================================================================
# PESTAÑA 3: MOVIMIENTOS
# =============================================================================
with tab_movimientos:
    st.header("📋 Historial de Movimientos")

    # --- Sidebar con filtros ---
    with st.sidebar:
        st.subheader("🔍 Filtrar Movimientos")

        if st.button("Actualizar", use_container_width=True):
            st.rerun()

        st.divider()

        # Filtro por tipo
        movement_type_filter = st.selectbox(
            "Tipo de movimiento",
            options=["Todos", "entrada", "salida"],
        )

        # Filtro por producto
        products = list_products()
        product_options = {p["name"]: p["id"] for p in products}
        selected_product = st.selectbox(
            "Producto",
            options=["Todos"] + list(product_options.keys()),
        )

        # Filtro por fechas
        st.divider()
        start_date = st.date_input("Desde", value=None)
        end_date = st.date_input("Hasta", value=None)

        # Convertir fechas a string
        start_date_str = start_date.strftime("%Y-%m-%d") if start_date else None
        end_date_str = end_date.strftime("%Y-%m-%d") if end_date else None

        st.divider()

        # Estadísticas de movimientos
        mov_stats = get_movement_stats()
        st.metric("Total Movimientos", mov_stats["total_movements"])
        st.metric("Entradas", mov_stats["entries"])
        st.metric("Salidas", mov_stats["outputs"])

    # --- Obtener movimientos filtrados ---
    product_id_filter = product_options.get(selected_product) if selected_product != "Todos" else None
    type_filter = movement_type_filter if movement_type_filter != "Todos" else None

    movements = get_movements(
        product_id=product_id_filter,
        movement_type=type_filter,
        start_date=start_date_str,
        end_date=end_date_str,
        limit=500,
    )

    # --- Tabla de movimientos ---
    if movements:
        # Determinar color por tipo
        type_colors = {"entrada": "🟢", "salida": "🔴"}

        st.dataframe(
            {
                "ID": [m["id"] for m in movements],
                "Fecha": [m["created_at"] for m in movements],
                "Producto": [m["product_name"] for m in movements],
                "Tipo": [f"{type_colors.get(m['movement_type'], '')} {m['movement_type'].capitalize()}" for m in movements],
                "Cantidad": [m["quantity"] for m in movements],
                "Motivo": [m["reason"] or "-" for m in movements],
            },
            hide_index=True,
            use_container_width=True,
            height=500,
        )

        # Exportar movimientos
        csv_mov = "ID,Fecha,Producto,Tipo,Cantidad,Motivo\n" + "\n".join(
            f"{m['id']},{m['created_at']},{m['product_name']},{m['movement_type']},{m['quantity']},{m['reason'] or ''}"
            for m in movements
        )
        st.download_button(
            "📥 Exportar Movimientos CSV",
            csv_mov,
            "movimientos.csv",
            mime="text/csv",
            use_container_width=True,
        )
    else:
        st.info("ℹ️ No hay movimientos que mostrar con los filtros seleccionados.")

    st.divider()

    # --- Registrar nuevo movimiento ---
    st.subheader("➕ Registrar Movimiento")

    col_mov1, col_mov2 = st.columns(2)

    with col_mov1:
        with st.expander("🟢 Registrar Entrada", expanded=False):
            entry_product = st.selectbox(
                "Producto",
                options=list(product_options.keys()),
                key="entry_product"
            )
            entry_qty = st.number_input("Cantidad", min_value=1, step=1, key="entry_qty")
            entry_reason = st.text_area("Motivo (opcional)", placeholder="Ej: Compra a proveedor", key="entry_reason")

            if st.button("Registrar Entrada", use_container_width=True, key="btn_entry"):
                prod_id = product_options[entry_product]
                try:
                    register_movement(prod_id, "entrada", entry_qty, entry_reason or "Entrada manual")
                    st.success(f"✅ Entrada de {entry_qty} unidades registrada.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

    with col_mov2:
        with st.expander("🔴 Registrar Salida", expanded=False):
            output_product = st.selectbox(
                "Producto",
                options=list(product_options.keys()),
                key="output_product"
            )
            output_qty = st.number_input("Cantidad", min_value=1, step=1, key="output_qty")
            output_reason = st.text_area("Motivo (opcional)", placeholder="Ej: Venta, merma, etc.", key="output_reason")

            if st.button("Registrar Salida", use_container_width=True, key="btn_output"):
                prod_id = product_options[output_product]
                try:
                    register_movement(prod_id, "salida", output_qty, output_reason or "Salida manual")
                    st.success(f"✅ Salida de {output_qty} unidades registrada.")
                    st.rerun()
                except ValueError as e:
                    st.error(f"❌ Stock insuficiente: {str(e)}")
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")

# =============================================================================
# PESTAÑA 4: ASISTENTE IA
# =============================================================================
with tab_chat:
    st.header("💬 Asistente Inteligente")
    st.caption("Consulta datos, pide resúmenes o busca productos usando lenguaje natural.")

    # Mostrar historial de chat (solo mensajes con contenido para el usuario)
    for message in st.session_state.messages:
        # Solo mostrar si el rol es usuario o asistente Y si tiene contenido de texto
        if message["role"] in ["user", "assistant"] and message.get("content"):
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    # Entrada del chat
    if prompt := st.chat_input("¿Qué deseas saber sobre el inventario? (Ej: ¿Cuáles son los productos con stock bajo?)"):
        # Añadir mensaje del usuario al historial
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Mostrar el mensaje del usuario inmediatamente
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generar respuesta de la IA
        with st.chat_message("assistant"):
            with st.spinner("Consultando inventario..."):
                response = ai_assistant.get_ai_response(st.session_state.messages)
                st.markdown(response)
        
        # Añadir respuesta de la IA al historial
        st.session_state.messages.append({"role": "assistant", "content": response})
