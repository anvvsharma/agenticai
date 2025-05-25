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

# Create a user instance
user = User(
    id=1, 
    name="John Doe", 
    email="john.doe@example.com",
    address=Address(
        street="123 Main St",
        city="AnyTown",
        state='CA',
        zip="12345"
    )
    )

#print(user) # Output ; User Details

print(user.model_dump_json(indent=2))
