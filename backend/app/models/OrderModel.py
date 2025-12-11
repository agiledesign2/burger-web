from sqlalchemy import (
    Column,
    Integer,
    #PrimaryKeyConstraint,
    String,
    ForeignKey
)
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship

# Importing OrderItem directly creates a circular import.  Use a string
# forward reference in the relationship() call instead.
# from models.OrderItemModel import OrderItem
from models.BaseModel import EntityMeta, BaseModel

class Order(EntityMeta, BaseModel):
    __tablename__ = "orders"
    
    id: int = Column(Integer, primary_key=True)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    total_amount: float = Column(DECIMAL(10, 2))
    status: str = Column(String(20), default="created")

    # Relationships (Lazy load by default)
    # ``default_factory`` is a dataclass feature and not supported by
    # SQLAlchemy relationships.  The relationship is lazy‑loaded by
    # default, so we simply omit the argument.
    items = relationship("OrderItem", back_populates="order", lazy="selectin")
    
    def normalize(self):
        return {
            "id": self.id.__str__(),
            "user_id": self.user_id.__str__(),
            "total_amount": float(self.total_amount.__str__()),
            "status": self.status.__str__(),
            "items": [item.normalize() for item in self.items]
        }
