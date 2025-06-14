
import os
from pydantic import BaseModel, Field
from groq import Groq
import json
from dotenv import load_dotenv
from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from typing import Dict, Any

# Load environment variables from .env file
load_dotenv()

class Product(BaseModel):
    name: str = Field(description="The name of the product")
    details: str = Field(description="Detailed description of the product")
    price: int = Field(description="Price of the product in dollars")

class Query(BaseModel):
    query: str = Field(description="The product query from user")

# Initialize Groq with LangChain
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")

# Initialize LangChain ChatGroq
llm = ChatGroq(
    api_key=groq_api_key,
    model="llama-3.1-8b-instant",
    temperature=0.7
)

# Initialize the JSON output parser
parser=JsonOutputParser(pydantic_object=Product)
#print(parser.get_format_instructions())
    
# Alternative implementation using JsonOutputFunctionsParser directly
def ask_product_question_with_parser(question: str) -> Product:
    """Alternative implementation using JsonOutputParser directly."""
  
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system","You are an expert AI Engineer.Provide the response in json.Provide me answer based on the question"),
            ("human", """Please provide information about: {query}"
             Product_Name: ***,
             Device_Details: ***,
             Phone_Price: ***
             """)
        ]
    )    
    # Create chain with JsonOutputParser
    chain = prompt | llm | parser
 
    try:

        response = chain.invoke({
            "query": question,
            "format_instructions": parser.get_format_instructions()
        })
        
        print(f"Raw response: {response}")

        # Convert response to Product object with robust field extraction
            
    except Exception as e:
        print(f"Error in parsing: {e}")
        return Product(
            name="Error",
            details=f"Failed to get product information: {str(e)}",
            price=0
        )

def handle_query(query_json: str) -> str:
    """Handle JSON query input and return JSON product output."""
    try:
        # Parse input JSON
        query = Query.model_validate(query_json)
        
        # Get product information
        product = ask_product_question_with_parser(query.query)
        
        # Return product as JSON
        return product.model_validate_json(indent=2)


    except Exception as e:
        # Return error as JSON
        error_response = {"error": str(e)}
        return json.dumps(error_response, indent=2)


# Example usage
if __name__ == "__main__":
    # Show format instructions
    print("Format Instructions from JsonOutputParser:")
    #print(parser.get_format_instructions())
    #print("\n" + "="*50 + "\n")
    
    query_json = '{"query": "iPhone 14"}'
    print(f"query: {query_json}")
    print("\n" + "="*30 + "\n")
    
    # Parse the query and call the function
    query = Query.model_validate_json(query_json)
    result = ask_product_question_with_parser(query.query)
    
    #print(f"Returned Product Object: {result}")
    #print(f"Product Name: {result.name}")
    #print(f"Product Details: {result.details}")
    #print(f"Product Price: {result.price}")
    
    
    # Also test the complete JSON workflow
    json_result = handle_query(query_json)
    print("Complete JSON Result:")
    print(json_result)