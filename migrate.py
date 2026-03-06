"""
Script de migración para actualizar la base de datos existente.
Agrega las nuevas columnas a la tabla products y crea la tabla movements.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "inventory.db"


def migrate():
    """Ejecuta la migración de la base de datos."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("Iniciando migracion de base de datos...")

    try:
        # 1. Agregar columnas a products (si no existen)
        columns_to_add = [
            ("category", "TEXT DEFAULT 'General'"),
            ("supplier", "TEXT"),
            ("min_stock", "INTEGER DEFAULT 10"),
            ("sku", "TEXT"),  # Sin UNIQUE, SQLite no lo permite en ALTER TABLE
            ("image_url", "TEXT"),
        ]

        for col_name, col_def in columns_to_add:
            try:
                cursor.execute(f"ALTER TABLE products ADD COLUMN {col_name} {col_def}")
                print(f"  Columna '{col_name}' agregada.")
            except sqlite3.OperationalError as e:
                if "duplicate column" in str(e).lower():
                    print(f"  Columna '{col_name}' ya existe.")
                else:
                    raise

        # 2. Crear tabla movements (si no existe)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS movements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                movement_type TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                reason TEXT,
                created_at DATETIME NOT NULL,
                FOREIGN KEY (product_id) REFERENCES products(id)
            )
        """)
        print("  Tabla 'movements' creada/verificada.")

        # 3. Actualizar productos existentes con valores por defecto
        cursor.execute("UPDATE products SET category = 'General' WHERE category IS NULL")
        cursor.execute("UPDATE products SET min_stock = 10 WHERE min_stock IS NULL")
        print("  Valores por defecto aplicados a productos existentes.")

        conn.commit()
        print("\nMigracion completada exitosamente!")

    except Exception as e:
        conn.rollback()
        print(f"\nError durante la migracion: {e}")
        raise

    finally:
        conn.close()


if __name__ == "__main__":
    migrate()
