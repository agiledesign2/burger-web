from sqlalchemy import (
    Column,
    Integer,
    #PrimaryKeyConstraint,
    String,
    Decimal,
    ForeignKey
)
from sqlalchemy.orm import relationship

from OrderItemModel import OrderItem
from models.BaseModel import EntityMeta, BaseModel
from typing import List, Optional

class Order(EntityMeta, BaseModel):
    __tablename__ = "orders"
    
    id: int = Column(Integer, primary_key=True, init=False)
    user_id: int = Column(Integer, ForeignKey("users.id"))
    total_amount: float = Column(Decimal(10, 2))
    status: str = Column(String(20), default="created")

    # Relationships (Lazy load by default)
    items: List["OrderItem"] = relationship(
        back_populates="order", default_factory=list, lazy="selectin"
    )
    
    def normalize(self):
        return {
            "id": self.id.__str__(),
            "user_id": self.user_id.__str__(),
            "total_amount": float(self.total_amount.__str__()),
            "status": self.status.__str__(),
            "items": [item.normalize() for item in self.items]
        }
