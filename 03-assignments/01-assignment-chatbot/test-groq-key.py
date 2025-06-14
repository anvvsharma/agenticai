from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("✅ Available models:")
models = client.models.list()
for model in models.data:
    print("-", model.id)
