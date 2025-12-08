from sqlalchemy import (
    Column,
    Integer,
    #PrimaryKeyConstraint,
    Decimal,
    ForeignKey
)
from sqlalchemy.orm import relationship

from models.OrderModel import Order
from models.BaseModel import EntityMeta, BaseModel
from typing import Optional

class OrderItem(EntityMeta, BaseModel):
    __tablename__ = "order_items"
    
    id: int = Column(primary_key=True, init=False)
    order_id: int = Column(ForeignKey("orders.id"), init=False)
    product_id: int = Column(ForeignKey("products.id"))
    quantity: int = Column(Integer, default=1)
    total_amount: float = Column(Decimal(10, 2)) # Snapshot of price
    
    order: Order = relationship(back_populates="items", init=False)
    
    def normalize(self):
        return {
            "id": self.id.__str__(),
            "order_id": self.order_id.__str__(),
            "product_id": self.product_id.__str__(),
            "quantity": int(self.quantity.__str__()),
            "total_amount": float(self.total_amount.__str__()),
            "order": self.order.normalize()
        }
