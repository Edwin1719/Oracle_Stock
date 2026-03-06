from typing import List, Optional
from datetime import datetime

from sqlalchemy import func
from models import Product, Movement
from db import get_session


# Helper to serialize Product objects
def _product_to_dict(prod: Product) -> dict:
    return {
        "id": prod.id,
        "name": prod.name,
        "price": prod.price,
        "quantity": prod.quantity,
        "category": prod.category,
        "supplier": prod.supplier,
        "min_stock": prod.min_stock,
        "sku": prod.sku,
        "image_url": prod.image_url,
    }


# Helper to serialize Movement objects
def _movement_to_dict(mov: Movement) -> dict:
    return {
        "id": mov.id,
        "product_id": mov.product_id,
        "product_name": mov.product.name if mov.product else "Desconocido",
        "movement_type": mov.movement_type,
        "quantity": mov.quantity,
        "reason": mov.reason,
        "created_at": mov.created_at.strftime("%Y-%m-%d %H:%M:%S") if mov.created_at else None,
    }


# =============================================================================
# CRUD DE PRODUCTOS (funciones existentes mejoradas)
# =============================================================================

def add_product(
    name: str,
    price: float,
    quantity: int,
    category: str = "General",
    supplier: str = None,
    min_stock: int = 10,
    sku: str = None,
    image_url: str = None,
) -> dict:
    """Create a new product record in the database.

    Returns a dict representation of the created product.
    """
    with get_session() as session:
        prod = Product(
            name=name,
            price=price,
            quantity=quantity,
            category=category,
            supplier=supplier,
            min_stock=min_stock,
            sku=sku,
            image_url=image_url,
        )
        session.add(prod)
        session.flush()

        # Registrar movimiento de entrada inicial
        if quantity > 0:
            movement = Movement(
                product_id=prod.id,
                movement_type="entrada",
                quantity=quantity,
                reason="Creación de producto",
                created_at=datetime.now(),
            )
            session.add(movement)

        return _product_to_dict(prod)


def remove_product(prod_id: int) -> bool:
    """Delete the product with the given id.

    Returns True if a record was deleted, False if no such id existed.
    """
    with get_session() as session:
        prod = session.get(Product, prod_id)
        if not prod:
            return False
        session.delete(prod)
        return True


def update_product(
    prod_id: int,
    *,
    price: Optional[float] = None,
    quantity: Optional[int] = None,
    category: Optional[str] = None,
    supplier: Optional[str] = None,
    min_stock: Optional[int] = None,
    sku: Optional[str] = None,
    image_url: Optional[str] = None,
) -> Optional[dict]:
    """Update fields of the product.

    Returns the updated product dict or None if no such id.
    """
    with get_session() as session:
        prod = session.get(Product, prod_id)
        if not prod:
            return None
        if price is not None:
            prod.price = price
        if quantity is not None:
            prod.quantity = quantity
        if category is not None:
            prod.category = category
        if supplier is not None:
            prod.supplier = supplier
        if min_stock is not None:
            prod.min_stock = min_stock
        if sku is not None:
            prod.sku = sku
        if image_url is not None:
            prod.image_url = image_url
        return _product_to_dict(prod)


def list_products() -> List[dict]:
    """Return all products as a list of dicts."""
    with get_session() as session:
        prods = session.query(Product).all()
        return [_product_to_dict(p) for p in prods]


def get_product_by_id(prod_id: int) -> Optional[dict]:
    """Return a single product by ID."""
    with get_session() as session:
        prod = session.get(Product, prod_id)
        return _product_to_dict(prod) if prod else None


# =============================================================================
# FUNCIONES DE FILTRO Y BÚSQUEDA
# =============================================================================

def get_products_by_category(category: str) -> List[dict]:
    """Return products filtered by category."""
    with get_session() as session:
        prods = session.query(Product).filter(Product.category == category).all()
        return [_product_to_dict(p) for p in prods]


def get_categories() -> List[str]:
    """Return list of unique categories."""
    with get_session() as session:
        categories = session.query(Product.category).distinct().all()
        return [c[0] for c in categories if c[0]]


def search_products(search_term: str, category: str = None) -> List[dict]:
    """Search products by name with optional category filter."""
    with get_session() as session:
        query = session.query(Product).filter(
            Product.name.ilike(f"%{search_term}%")
        )
        if category:
            query = query.filter(Product.category == category)
        prods = query.all()
        return [_product_to_dict(p) for p in prods]


# =============================================================================
# FUNCIONES PARA DASHBOARD
# =============================================================================

def get_inventory_stats() -> dict:
    """Return general inventory statistics."""
    from sqlalchemy import func

    with get_session() as session:
        total_products = session.query(Product).count()

        # Calculate total inventory value
        products = session.query(Product).all()
        total_value = sum(p.price * p.quantity for p in products)

        # Products with low stock (below their min_stock threshold)
        low_stock_count = session.query(Product).filter(
            Product.quantity < Product.min_stock
        ).count()

        # Products out of stock
        out_of_stock_count = session.query(Product).filter(Product.quantity == 0).count()

        # Average price
        avg_price_result = session.query(func.avg(Product.price)).scalar()
        avg_price = avg_price_result if avg_price_result else 0.0

        # Products by category
        category_stats = {}
        for p in products:
            cat = p.category or "General"
            if cat not in category_stats:
                category_stats[cat] = {"count": 0, "value": 0}
            category_stats[cat]["count"] += 1
            category_stats[cat]["value"] += p.price * p.quantity

        return {
            "total_products": total_products,
            "total_value": round(total_value, 2),
            "low_stock_count": low_stock_count,
            "out_of_stock_count": out_of_stock_count,
            "avg_price": round(avg_price, 2),
            "category_stats": category_stats,
        }


def get_low_stock_products() -> List[dict]:
    """Return products with stock below their min_stock threshold."""
    with get_session() as session:
        prods = session.query(Product).filter(
            Product.quantity < Product.min_stock
        ).all()
        return [_product_to_dict(p) for p in prods]


def get_products_by_category_value() -> List[dict]:
    """Return products grouped by category with total value."""
    with get_session() as session:
        products = session.query(Product).all()
        category_data = {}

        for p in products:
            cat = p.category or "General"
            if cat not in category_data:
                category_data[cat] = {"count": 0, "value": 0, "products": []}
            category_data[cat]["count"] += 1
            category_data[cat]["value"] += p.price * p.quantity
            category_data[cat]["products"].append(p.name)

        return [
            {"category": cat, "count": data["count"], "value": round(data["value"], 2)}
            for cat, data in category_data.items()
        ]


# =============================================================================
# GESTIÓN DE MOVIMIENTOS
# =============================================================================

def register_movement(
    product_id: int,
    movement_type: str,
    quantity: int,
    reason: str = None,
) -> dict:
    """Register a new inventory movement.

    movement_type: 'entrada' or 'salida'
    Updates product quantity automatically.
    """
    with get_session() as session:
        prod = session.get(Product, product_id)
        if not prod:
            raise ValueError(f"Product with id {product_id} not found")

        # Validate movement
        if movement_type == "salida" and prod.quantity < quantity:
            raise ValueError(
                f"Stock insuficiente. Actual: {prod.quantity}, Solicitado: {quantity}"
            )

        # Update product quantity
        if movement_type == "entrada":
            prod.quantity += quantity
        else:
            prod.quantity -= quantity

        # Register movement
        movement = Movement(
            product_id=product_id,
            movement_type=movement_type,
            quantity=quantity,
            reason=reason,
            created_at=datetime.now(),
        )
        session.add(movement)
        session.flush()

        return _movement_to_dict(movement)


def get_movements(
    product_id: int = None,
    movement_type: str = None,
    start_date: str = None,
    end_date: str = None,
    limit: int = 100,
) -> List[dict]:
    """Get movements with optional filters.

    Dates should be in format 'YYYY-MM-DD'.
    """
    with get_session() as session:
        query = session.query(Movement).order_by(Movement.created_at.desc())

        if product_id:
            query = query.filter(Movement.product_id == product_id)

        if movement_type:
            query = query.filter(Movement.movement_type == movement_type)

        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(Movement.created_at >= start_dt)

        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            end_dt = end_dt.replace(hour=23, minute=59, second=59)
            query = query.filter(Movement.created_at <= end_dt)

        query = query.limit(limit)
        movements = query.all()

        return [_movement_to_dict(m) for m in movements]


def get_movement_stats() -> dict:
    """Return movement statistics."""
    with get_session() as session:
        total_movements = session.query(Movement).count()
        entries = session.query(Movement).filter(
            Movement.movement_type == "entrada"
        ).count()
        outputs = session.query(Movement).filter(
            Movement.movement_type == "salida"
        ).count()

        # Total quantity moved
        total_entry_qty = session.query(Movement).filter(
            Movement.movement_type == "entrada"
        ).with_entities(func.sum(Movement.quantity)).scalar() or 0

        total_output_qty = session.query(Movement).filter(
            Movement.movement_type == "salida"
        ).with_entities(func.sum(Movement.quantity)).scalar() or 0

        return {
            "total_movements": total_movements,
            "entries": entries,
            "outputs": outputs,
            "total_entry_qty": total_entry_qty,
            "total_output_qty": total_output_qty,
        }


# =============================================================================
# EXPORTAR DATOS
# =============================================================================

def export_to_dict() -> List[dict]:
    """Export all products as list of dicts (for CSV/Excel)."""
    return list_products()
