from db import engine
from models import Base, Product
from repository import add_product

# Create tables if they don't exist
Base.metadata.create_all(engine)

# Predefined tech products with categories and suppliers
PREDEFINED_PRODUCTS = [
    {"name": "Laptop Dell Inspiron 15", "price": 999.99, "quantity": 20, "category": "Laptops", "supplier": "Dell Inc.", "sku": "DELL-INS15"},
    {"name": "iPhone 14 Pro", "price": 699.99, "quantity": 35, "category": "Smartphones", "supplier": "Apple Inc.", "sku": "APL-IPH14P"},
    {"name": "iPad Air", "price": 399.99, "quantity": 15, "category": "Tablets", "supplier": "Apple Inc.", "sku": "APL-IPADAIR"},
    {"name": "Monitor Samsung 27\"", "price": 199.99, "quantity": 25, "category": "Monitores", "supplier": "Samsung", "sku": "SAM-MON27"},
    {"name": "Teclado Mecanico RGB", "price": 49.99, "quantity": 40, "category": "Perifericos", "supplier": "Logitech", "sku": "LOG-KB-RGB"},
    {"name": "Mouse Inalambrico", "price": 29.99, "quantity": 50, "category": "Perifericos", "supplier": "Logitech", "sku": "LOG-MSE-WL"},
    {"name": "Impresora HP LaserJet", "price": 149.99, "quantity": 10, "category": "Impresoras", "supplier": "HP Inc.", "sku": "HP-LJ-Pro"},
    {"name": "Router WiFi 6", "price": 79.99, "quantity": 30, "category": "Redes", "supplier": "TP-Link", "sku": "TPL-WIFI6"},
    {"name": "Disco Duro Externo 1TB", "price": 89.99, "quantity": 22, "category": "Almacenamiento", "supplier": "Western Digital", "sku": "WD-EXT1TB"},
    {"name": "Hub USB-C 7 puertos", "price": 59.99, "quantity": 18, "category": "Accesorios", "supplier": "Anker", "sku": "ANK-HUB7P"},
    {"name": "Tableta Grafica Wacom", "price": 299.99, "quantity": 12, "category": "Perifericos", "supplier": "Wacom", "sku": "WAC-INTUOS"},
    {"name": "Audifonos Bluetooth Sony", "price": 129.99, "quantity": 45, "category": "Audio", "supplier": "Sony", "sku": "SNY-BT-NC"},
    {"name": "Webcam Logitech HD", "price": 99.99, "quantity": 28, "category": "Perifericos", "supplier": "Logitech", "sku": "LOG-C920"},
    {"name": "Microfono USB Blue", "price": 149.99, "quantity": 14, "category": "Audio", "supplier": "Blue Yeti", "sku": "BLUE-YETI"},
    {"name": "Reloj Inteligente Garmin", "price": 199.99, "quantity": 26, "category": "Wearables", "supplier": "Garmin", "sku": "GAR-VENU"},
]


def seed():
    # Check if database already has products
    from repository import list_products
    existing = list_products()
    if existing:
        print(f"Database already contains {len(existing)} products. Skipping seeding.")
        return

    for prod in PREDEFINED_PRODUCTS:
        add_product(**prod)
    print(f"Seeded {len(PREDEFINED_PRODUCTS)} products into the database.")


if __name__ == "__main__":
    seed()
