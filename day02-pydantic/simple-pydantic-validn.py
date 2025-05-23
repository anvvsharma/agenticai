from pydantic import BaseModel, ValidationError

class User(BaseModel):
    id: int
    name: str
    email: str

try:
    user = User(id="string", name="John Doe", email="john.doe@example.com")
except ValidationError as e:
    print("Validation Error : ", e) # Output : value is not a valid integer
