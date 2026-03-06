from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Enum
from sqlalchemy.orm import declarative_base, relationship
import enum

Base = declarative_base()


class MovementType(enum.Enum):
    """Types of inventory movements."""
    ENTRY = "entrada"
    OUTPUT = "salida"


class Product(Base):
    """Represents a technology product in inventory."""

    __tablename__ = "products"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False, default=0)
    category = Column(String, nullable=True, default="General")
    supplier = Column(String, nullable=True)
    min_stock = Column(Integer, nullable=True, default=10)
    sku = Column(String, nullable=True, unique=True)
    image_url = Column(String, nullable=True)

    # Relationship with movements
    movements = relationship("Movement", back_populates="product", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"<Product id={self.id} name={self.name!r} category={self.category} price={self.price} qty={self.quantity}>"


class Movement(Base):
    """Represents an inventory movement (entry or output)."""

    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    movement_type = Column(String, nullable=False)  # 'entrada' or 'salida'
    quantity = Column(Integer, nullable=False)
    reason = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False)

    # Relationship with product
    product = relationship("Product", back_populates="movements")

    def __repr__(self) -> str:
        return f"<Movement id={self.id} product_id={self.product_id} type={self.movement_type} qty={self.quantity}>"
