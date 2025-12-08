from sqlalchemy import (
    Column,
    Integer,
    #PrimaryKeyConstraint,
    String,
    Boolean,
    Decimal,
    Text
)
from models.BaseModel import EntityMeta, BaseModel
from typing import Optional

class Product(EntityMeta, BaseModel):
    __tablename__ = "products"
    
    id: int = Column(Integer, primary_key=True, init=False)
    name: str = Column(String(100))
    description: Optional[str] = Column(Text, default=None)
    price: float = Column(Decimal(10, 2))
    category: str = Column(String(50)) # burger, side, drink, addon
    image_url: Optional[str] = Column(String(255), default=None)
    in_stock: bool = Column(Boolean, default=True)

    #PrimaryKeyConstraint(id)
    
    def normalize(self):
        return {
            "id": self.id.__str__(),
            "name": self.name.__str__(),
            "description": self.description.__str__(),
            "price": float(self.price.__str__()),
            "category": self.category.__str__(),
            "image_url": self.image_url.__str__(),
            "in_stock": self.in_stock.__str__()
        }
