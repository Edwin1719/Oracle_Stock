"""
Script para actualizar productos existentes con categorías y proveedores ficticios.
"""

from repository import update_product, list_products

# Datos ficticios para actualizar productos
PRODUCT_UPDATES = {
    "Laptop": {"category": "Laptops", "supplier": "Dell Inc.", "sku": "DELL-001", "min_stock": 5},
    "Smartphone": {"category": "Smartphones", "supplier": "Samsung Electronics", "sku": "SAM-002", "min_stock": 10},
    "Tablet": {"category": "Tablets", "supplier": "Apple Inc.", "sku": "APL-003", "min_stock": 8},
    "Monitor": {"category": "Monitores", "supplier": "LG Electronics", "sku": "LG-004", "min_stock": 10},
    "Keyboard": {"category": "Perifericos", "supplier": "Logitech", "sku": "LOG-005", "min_stock": 15},
    "Mouse": {"category": "Perifericos", "supplier": "Logitech", "sku": "LOG-006", "min_stock": 20},
    "Printer": {"category": "Impresoras", "supplier": "HP Inc.", "sku": "HP-007", "min_stock": 5},
    "Router": {"category": "Redes", "supplier": "TP-Link", "sku": "TPL-008", "min_stock": 12},
    "External Hard Drive": {"category": "Almacenamiento", "supplier": "Western Digital", "sku": "WD-009", "min_stock": 10},
    "USB-C Hub": {"category": "Accesorios", "supplier": "Anker", "sku": "ANK-010", "min_stock": 15},
    "Graphics Tablet": {"category": "Perifericos", "supplier": "Wacom", "sku": "WAC-011", "min_stock": 5},
    "Headphones": {"category": "Audio", "supplier": "Sony", "sku": "SNY-012", "min_stock": 20},
    "Webcam": {"category": "Perifericos", "supplier": "Logitech", "sku": "LOG-013", "min_stock": 10},
    "Microphone": {"category": "Audio", "supplier": "Blue Yeti", "sku": "BLUE-014", "min_stock": 8},
    "Smartwatch": {"category": "Wearables", "supplier": "Garmin", "sku": "GAR-015", "min_stock": 10},
    "Auriculares Samsung": {"category": "Audio", "supplier": "Samsung Electronics", "sku": "SAM-016", "min_stock": 15},
}


def update_products_data():
    """Actualiza todos los productos con categorías y proveedores ficticios."""
    products = list_products()
    
    print(f"Total de productos encontrados: {len(products)}")
    print("-" * 60)
    
    updated_count = 0
    
    for prod in products:
        prod_name = prod["name"]
        
        if prod_name in PRODUCT_UPDATES:
            update_data = PRODUCT_UPDATES[prod_name]
            
            update_product(
                prod["id"],
                category=update_data["category"],
                supplier=update_data["supplier"],
                sku=update_data["sku"],
                min_stock=update_data["min_stock"],
            )
            
            print(f"[OK] {prod_name}")
            print(f"   Categoría: {update_data['category']}")
            print(f"   Proveedor: {update_data['supplier']}")
            print(f"   SKU: {update_data['sku']}")
            print(f"   Stock mínimo: {update_data['min_stock']}")
            print()
            
            updated_count += 1
        else:
            print(f"[INFO] {prod_name} - No hay datos para actualizar")
    
    print("-" * 60)
    print(f"Productos actualizados: {updated_count} de {len(products)}")
    print("\nActualizacion completada!")


if __name__ == "__main__":
    update_products_data()
