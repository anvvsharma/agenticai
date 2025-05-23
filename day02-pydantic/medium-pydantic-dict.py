from pydantic import BaseModel
from typing import List, Dict
import json
from pprint import pprint

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
    metadata={"created_at": "2025-05-21T12:00:00"}
    )

print(user.model_dump_json(indent=2))
