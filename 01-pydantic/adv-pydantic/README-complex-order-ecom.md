## import below libraries

    Pydantic Models for E-commerce Orders
    from datetime import datetime, date
    from typing import Optional, List, Dict, Union, Literal, Any
    from enum import Enum
    from pydantic import BaseModel, Field, EmailStr, field_validator, model_validator, ValidationError
    from pydantic import constr, conint, confloat
    from uuid import UUID, uuid4

## Core Models

### Money Model with Validation ###
```python
class Money(BaseModel):
    """Represents a monetary value with currency."""
    amount: confloat(ge=0)  # Ensure amount is a positive float
    currency: constr(min_length=3, max_length=3)  # Currency code (e.g., "USD")

    def __str__(self):
        return f"{self.amount} {self.currency}"
Category Model
class Category(BaseModel):
    """Represents a product category."""
    id: int
    name: str
    slug: str
    parent_id: Optional[int] = None  # Optional parent category ID
Order Status and Item Models
class OrderStatus(str, Enum):
    """Order status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

class OrderItem(BaseModel):
    """Represents an order item."""
    # product_id: UUID
    # variant_id: Optional[UUID] = None
    quantity: conint(gt=0)  # Ensure quantity is a positive integer
    unit_price: Money

    @property
    def total_price(self) -> Money:
        """Calculates the total price for this order item."""
        return Money(
            amount=self.quantity * self.unit_price.amount,
            currency=self.unit_price.currency
        )
Shipping and Billing Address Models
class ShippingAddress(BaseModel):
    """Represents a shipping address."""
    recipient_name: str
    company: Optional[str] = None
    address_line1: str
    address_line2: Optional[str] = None
    city: str
    state: Optional[str] = None
    postal_code: str
    country: str
    phone: Optional[str] = None
Complex Order Model with Financial Validation
class Order(BaseModel):
    """Represents a customer order."""
    id: UUID = Field(default_factory=uuid4)  # Unique order ID
    order_number: str
    customer_id: UUID
    status: OrderStatus = OrderStatus.PENDING
    items: List[OrderItem]
    shipping_address: ShippingAddress
    billing_address: ShippingAddress
    subtotal: Money
    tax_amount: Money
    shipping_cost: Money
    discount_amount: Money = Field(default=Money(amount=0, currency="USD"))
    total: Money
    notes: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: Optional[datetime] = None

    # Example of a field validator (uncomment to use)
    # @field_validator('order_number')
    # @classmethod
    # def validate_order_number(cls, v):
    #     if not v.startswith('ORD-'):
    #         raise ValueError('Order Number must start with "ORD-"')
    #     return v
Usage Example: Define Data for Objects
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

```

#### This code defines a set of Pydantic models for an e-commerce platform, including:
#### Money: Represents a monetary value with currency.
#### Category: Represents a product category.
#### OrderStatus: Order status enumeration. 
#### OrderItem: Represents an order item. 
#### ShippingAddress: Represents a shipping address.
#### Order: Represents a customer order.
** The example usage demonstrates how to create instances of these models and print a complex order in JSON format. **
