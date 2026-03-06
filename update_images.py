"""
Script para actualizar productos con URLs de imagenes ficticias.
Usa imagenes de placeholder.co para demostracion.
"""

from repository import update_product, list_products

# URLs de imagenes ficticias para cada producto
# Usamos placeholder.co con colores y texto para simular imagenes de productos
PRODUCT_IMAGES = {
    "Laptop": {
        "image_url": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=300&fit=crop"
    },
    "Smartphone": {
        "image_url": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=400&h=300&fit=crop"
    },
    "Tablet": {
        "image_url": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=300&fit=crop"
    },
    "Monitor": {
        "image_url": "https://images.unsplash.com/photo-1527443224154-c4a3942d3acf?w=400&h=300&fit=crop"
    },
    "Keyboard": {
        "image_url": "https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=400&h=300&fit=crop"
    },
    "Mouse": {
        "image_url": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=300&fit=crop"
    },
    "Printer": {
        "image_url": "https://images.unsplash.com/photo-1612815154858-60aa4c59eaa6?w=400&h=300&fit=crop"
    },
    "Router": {
        "image_url": "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=400&h=300&fit=crop"
    },
    "External Hard Drive": {
        "image_url": "https://images.unsplash.com/photo-1597872250977-479a2b124c8e?w=400&h=300&fit=crop"
    },
    "USB-C Hub": {
        "image_url": "https://images.unsplash.com/photo-1625842268584-8f3296236761?w=400&h=300&fit=crop"
    },
    "Graphics Tablet": {
        "image_url": "https://images.unsplash.com/photo-1616169047064-4c0008e205ca?w=400&h=300&fit=crop"
    },
    "Headphones": {
        "image_url": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=300&fit=crop"
    },
    "Webcam": {
        "image_url": "https://images.unsplash.com/photo-1621252179027-94459d27d3ee?w=400&h=300&fit=crop"
    },
    "Microphone": {
        "image_url": "https://images.unsplash.com/photo-1590608315707-9909578e428b?w=400&h=300&fit=crop"
    },
    "Smartwatch": {
        "image_url": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=400&h=300&fit=crop"
    },
    "Auriculares Samsung": {
        "image_url": "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=300&fit=crop"
    },
}


def update_product_images():
    """Actualiza todos los productos con URLs de imagenes."""
    products = list_products()
    
    print(f"Total de productos encontrados: {len(products)}")
    print("-" * 60)
    
    updated_count = 0
    
    for prod in products:
        prod_name = prod["name"]
        
        if prod_name in PRODUCT_IMAGES:
            image_data = PRODUCT_IMAGES[prod_name]
            
            update_product(
                prod["id"],
                image_url=image_data["image_url"],
            )
            
            print(f"[OK] {prod_name}")
            print(f"   Imagen: {image_data['image_url'][:60]}...")
            print()
            
            updated_count += 1
        else:
            print(f"[INFO] {prod_name} - No hay imagen configurada")
    
    print("-" * 60)
    print(f"Productos actualizados: {updated_count} de {len(products)}")
    print("\nActualizacion de imagenes completada!")


if __name__ == "__main__":
    update_product_images()
