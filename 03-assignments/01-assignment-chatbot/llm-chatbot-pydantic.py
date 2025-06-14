import os
import argparse
from pydantic import BaseModel, ValidationError
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the expected product structure
class ProductInfo(BaseModel):
    product_name: str
    product_details: str
    tentative_price: int

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")
client = Groq(api_key=groq_api_key)

def ask_product_question(question: str) -> ProductInfo:
    prompt_text = (
        "You are a helpful assistant that provides information about products.\n"
        "When a user asks about a product, respond only in the following format:\n\n"
        "Product Name: <product name>\n"
        "Product Details: <product description>\n"
        "Tentative Price: <price in USD as integer>\n\n"
        f"User question: {question}"
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are a product assistant."},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.7,
    )

    reply = response.choices[0].message.content
    print("\nLLM Raw Reply:\n", reply)

    lines = [line.strip() for line in reply.strip().splitlines() if line.strip()]
    product_info = {}

    if lines:
        if lines[0].lower().startswith("product name:"):
            product_info["product_name"] = lines[0].split(":", 1)[1].strip()
        else:
            product_info["product_name"] = lines[0].rstrip(":").strip()
            lines = lines[1:]

    for line in lines:
        if line.lower().startswith("product details:"):
            product_info["product_details"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("tentative price:"):
            price_str = line.split(":", 1)[1].strip().replace("$", "").replace(",", "")
            try:
                product_info["tentative_price"] = int(price_str)
            except ValueError:
                product_info["tentative_price"] = None

    try:
        return ProductInfo(**product_info)
    except ValidationError as e:
        print("\n Validation Error:")
        for err in e.errors():
            print(f"- {err['loc'][0]}: {err['msg']}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ask about a product.")
    parser.add_argument("query", type=str, help="Product query (e.g., 'Tell me about iPhone 15')")
    args = parser.parse_args()

    product = ask_product_question(args.query)
    print("\n Parsed Product Info:\n", product.model_dump_json(indent=2))
