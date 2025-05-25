**Pydantic Examples: Simple, Medium, and Complex**
============================================

Pydantic is a Python library for building robust, scalable, and fast data models. It provides a simple and intuitive way to define data models, validate data, and generate JSON schema.

### **Step 1: Installation**

To start with Pydantic, install it using pip:

```bash
pip install pydantic
```

### **Simple Python Pydantic Examples**
------------------------------------

### **1. Basic Model**

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

# Create a user instance
user = User(id=1, name="John Doe", email="john.doe@example.com")

print(user)  # Output: id=1 name='John Doe' email='john.doe@example.com'
print(user.json())  # Output: {"id": 1, "name": "John Doe", "email": "john.doe@example.com"}
```

### **2. Validation**

```python
from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str
    email: str

try:
    user = User(id="string", name="John Doe", email="john.doe@example.com")
except ValidationError as e:
    print(e)  # Output: value is not a valid integer (type=type_error.integer)
```

### **Medium Python Pydantic Examples**
--------------------------------------

### **1. Nested Models**

```python
from pydantic import BaseModel

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip: str

class User(BaseModel):
    id: int
    name: str
    email: str
    address: Address

# Create a user instance with address
user = User(
    id=1,
    name="John Doe",
    email="john.doe@example.com",
    address=Address(street="123 Main St", city="Anytown", state="CA", zip="12345")
)

print(user)  
```

### **2. List and Dictionary Fields**

```python
from pydantic import BaseModel
from typing import List, Dict

class User(BaseModel):
    id: int
    name: str
    email: str
    tags: List[str]
    metadata: Dict[str, str]

# Create a user instance with list and dictionary fields
user = User(
    id=1,
    name="John Doe",
    email="john.doe@example.com",
    tags=["admin", "moderator"],
    metadata={"created_at": "2022-01-01T12:00:00"}
)

print(user)  
```

### **Complex Python Pydantic Examples**
--------------------------------------

### **1. Advanced Validation and Error Handling**

```python
from pydantic import BaseModel, validator
from datetime import datetime

class User(BaseModel):
    id: int
    name: str
    email: str
    created_at: datetime

    @validator("created_at")
    def created_at_must_be_in_past(cls, v):
        if v >= datetime.now():
            raise ValueError("created_at must be in the past")
        return v

try:
    user = User(id=1, name="John Doe", email="john.doe@example.com", created_at=datetime.now())
except ValueError as e:
    print(e)  # Output: created_at must be in the past
```

### **2. Using Pydantic with External Libraries (e.g., SQLAlchemy)**

```python
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

class UserPydantic(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# Assume you have a SQLAlchemy session
session = ... 

user = session.query(User).first()
user_pydantic = UserPydantic.from_orm(user)

print(user_pydantic)  
```
