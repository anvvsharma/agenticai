import os
import argparse
from pydantic import BaseModel, ValidationError
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Define the expected product structure
class ProductInfo(BaseModel):
    actor: str
    pre_condition: str
    basic_flow: str
    success_condition: str
    failure_condition: str
    post_condition: str
    technical_documentation: str
    usecase_name: str    

# Initialize Groq client
groq_api_key = os.getenv("GROQ_API_KEY")
if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")
client = Groq(api_key=groq_api_key)

def ask_order_question(question: str) -> ProductInfo:
    prompt_text = (
        "You are a helpful assistant that provides information about Order Use Cases.\n"
        "When a user asks about a usecases, respond only in the following format:\n\n"
        "Actors: <Actors involved in end to end functionality >\n"
        "Pre Condition: <pre-conditions>\n"
        "Basic Flow: <Specify step by step of integration of split lines in FOM and Synched back to EBS>\n\n"
        "Success Condition: <success condition>\n\n"
        "Failure Condition: <failure condition>\n\n"
        "Post Condition: <post condition>\n\n"
        "Technical Documentation: <Write Technical Document with above details using Actors, Pre Conditions, Basic Flow, Success Condition, Failure Condition, Post Condition>\n\n"        
        f"UseCase Name: {question}"
    )

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are the Fusion Order Management Functional Export and Oracle Integration Cloud Expert"},
            {"role": "user", "content": prompt_text}
        ],
        temperature=0.7,
    )

    reply = response.choices[0].message.content
    print("\nLLM Raw Reply:\n", reply)

    lines = [line.strip() for line in reply.strip().splitlines() if line.strip()]
    order_info = {
        "actor": "",
        "pre_condition": "",
        "basic_flow": "",
        "success_condition": "",
        "failure_condition": "",
        "post_condition": "",
        "technical_documentation": "",
        "usecase_name": question        
    }

    for line in lines:
        if line.lower().startswith("actors:"):
            order_info["actors"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("pre_condition:"):
            order_info["Pre Condition"] = line.split(":", 1)[1].strip()
        elif line.lower().startswith("Basic Flow:"):
            basic_flow = line.split(":", 1)[1].strip()
        elif line.lower().startswith("Success Condition:"):
            success_condition = line.split(":", 1)[1].strip()
        elif line.lower().startswith("Failure Condition:"):
            failure_condition = line.split(":", 1)[1].strip()
        elif line.lower().startswith("Post Condition:"):
            post_condition = line.split(":", 1)[1].strip()
        elif line.lower().startswith("Technical Documentation:"):
            technical_documentation = line.split(":", 1)[1].strip()
            

    try:
        return ProductInfo(**order_info)
    except ValidationError as e:
        print("\n Validation Error:")
        for err in e.errors():
            print(f"- {err['loc'][0]}: {err['msg']}")
        raise

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ask about a Order Use-Case.")
    parser.add_argument("query", type=str, help="Use-Case query (e.g., 'write about functional Use-Case')")
    args = parser.parse_args()

    order_info = ask_order_question(args.query)
    print("\n Parsed Order Info:\n", order_info.model_dump_json(indent=2))
