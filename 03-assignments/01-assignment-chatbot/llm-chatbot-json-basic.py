
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

# Initialize Groq with LangChain
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    raise ValueError("GROQ_API_KEY environment variable not set.")

class Query(BaseModel):
    query: str = Field(description="The Product query from user")

# Initialize LangChain ChatGroq
llm = ChatGroq(
    api_key=groq_api_key,
    model="llama-3.1-8b-instant",
    temperature=0.7
)

### Assisgnment ---Chatprompttemplate

### Prompt Engineering

prompt=ChatPromptTemplate.from_messages(
    [
        ("system","You are an expert AI Engineer.Provide the response in json.Provide me answer based on the question"),
        ("user","{input}")
    ]
)
print(prompt)

# Initialize the JSON output parser
parser=JsonOutputParser({input})
#print(parser.get_format_instructions())
    
# Alternative implementation using JsonOutputFunctionsParser directly
def ask_product_question_with_parser(question: str) -> Product:
    """Alternative implementation using JsonOutputParser directly."""
  
    prompt=ChatPromptTemplate.from_messages(
        [
            ("system","You are an expert AI Engineer.Provide the response in json.Provide me answer based on the question"),
            ("human", """Please provide information about: {query}"
             """)
        ]
    )    

    # Create chain with JsonOutputParser
    chain = prompt | llm | parser

    response=chain.invoke({"input":"Can you tell me about Langsmith?"})
    print(response)


    response = chain.invoke({
        "query": question,
        "format_instructions": parser.get_format_instructions()
    })
        
        #print(f"Raw response: {response}")

def handle_query(query_json: str) -> str:
    """Handle JSON query input and return JSON product output."""

    # Parse input JSON
    query = Query.model_validate_json(query_json)
    
    # Get product information
    product = ask_product_question_with_parser(query.query)
    
    # Return product as JSON
    return product.model_dump_json(indent=2)


# Example usage
if __name__ == "__main__":
    # Show format instructions
    
    query_json = '{"query": "iPhone 14"}'
    print(f"query: {query_json}")
    print("\n" + "="*30 + "\n")
    
    # Parse the query and call the function
    query = Query.model_validate_json(query_json)
    result = ask_product_question_with_parser(query.query)
      
    # Also test the complete JSON workflow
    json_result = handle_query(query_json)
    print("Complete JSON Result:")
    print(json_result)