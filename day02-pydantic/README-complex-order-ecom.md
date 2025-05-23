'''

from datetime import datetime, date
from typing import Optional, List, Dict, Union, Literal, Any
from enum import Enum
from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator, ValidationError
from pydantic import constr, conint, confloat
from uuid import UUID, uuid4
```
## Core Models

### Money Model with Validation ###
```
class Money(BaseModel):
    amount: confloat(ge=0)
    currency: constr(min_length=3, max_length=3)

    def __str__(self):
        return f"{self.amount} {self.currency}"
```
### Category Model ###
```
class Category(BaseModel):
    id: int
    name: str
    slug: str
    parent_id: Optional[int] = None
```
    
### Order Status and Item Models
```
class OrderStatus(str, Enum):
    PENDING     = "pending"
    CONFIRMED   ="confirmed"
    SHIPPED     = "shipped"
    DELIVERED   = "delivered"
    CANCELLED   = "cancelled"
```
### Order Status and Item Models ###
```
class OrderItem(BaseModel):
    # product_id: UUID
    # variant_id: Optional[UUID] = None
    quantity: conint(gt=0)
    unit_price: Money

    @property
    def total_price(self) -> Money:
        return Money(
            amount=self.quantity * self.unit_price.amount,
            currency=self.unit_price.currency
        )

class ShippingAddress(BaseModel):
    recipient_name: str
    company: Optional[str] = None
    address_line1:str
    address_line2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postal_code:str
    country: str
    phone: Optional[str] = None
```
### Complex Order Model with Financial Validation ###
```
class Order(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    order_number: str
    customer_id: UUID
    status: OrderStatus = OrderStatus.PENDING
    items: List[OrderItem]
    shipping_address: ShippingAddress
    ## billing_address: Optional[ShippingAddress] = None
    billing_address: ShippingAddress
    subtotal: Money
    tax_amount: Money
    shipping_cost: Money
    discount_amount: Money = Field(default=Money(amount=0, currency="USD"))
    total: Money
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    @field_validator('order_number')
    @classmethod
    def validate_order_number(cls, v):
        if not v.startswith('ORD-'):
            raise ValueError('Order Number must start with "ORD-"')
        return v
```
### Usage Example , define data for the Objects
```
categories = [
    Category(id=1, name="Electronics", slug="electronics"),
    Category(id=2, name="Computers", slug="computers", parent_id=1)
]

order_items = [
    OrderItem(
        # product_id=product.id,
        # variant_id=product.variants[0].id,
        quantity=1,
        unit_price=Money(amount=2499.00, currency="USD")
    )
]

shipping_address = ShippingAddress(
    recipient_name="John Smith",
    address_line1="123 Tech Street",
    city="San Francisco",
    state="CA",
    postal_code="94105",
    country="USA",
    phone="555-123-4567"
)

order = Order(
    order_number="ORD-2024-001",
    customer_id=uuid4(),
    items=order_items,
    shipping_address=shipping_address,
    billing_address=shipping_address,
    subtotal=Money(amount=2499.00, currency="USD"),
    tax_amount=Money(amount=224.91, currency="USD"),
    shipping_cost=Money(amount=15.00, currency="USD"),
    total=Money(amount=2738.91, currency="USD")
)

print("✓ Complex order created:")
print(order.model_dump_json(indent=0))

'''
