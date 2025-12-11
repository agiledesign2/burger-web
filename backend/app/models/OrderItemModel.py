from sqlalchemy import (
    Column,
    Integer,
    #PrimaryKeyConstraint,
    ForeignKey
)
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship

# Importing Order directly causes a circular import because OrderItemModel
# is imported by OrderModel.  Use a forward reference in the
# relationship() call instead of importing the class.
from models.BaseModel import EntityMeta, BaseModel

class OrderItem(EntityMeta, BaseModel):
    __tablename__ = "order_items"
    
    id: int = Column(primary_key=True)
    order_id: int = Column(ForeignKey("orders.id"))
    product_id: int = Column(ForeignKey("products.id"))
    quantity: int = Column(Integer, default=1)
    total_amount: float = Column(DECIMAL(10, 2)) # Snapshot of price
    
    order = relationship("Order", back_populates="items")
    
    def normalize(self):
        return {
            "id": self.id.__str__(),
            "order_id": self.order_id.__str__(),
            "product_id": self.product_id.__str__(),
            "quantity": int(self.quantity.__str__()),
            "total_amount": float(self.total_amount.__str__()),
            "order": self.order.normalize()
        }
