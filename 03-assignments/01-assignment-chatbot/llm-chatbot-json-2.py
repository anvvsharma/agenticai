# CORRECT IMPORT - Use this for newer versions of LangChain
from langchain_core.output_parsers.json import JsonOutputParser
from langchain_core.exceptions import OutputParserException
from pydantic import BaseModel, Field
from typing import Any, Dict, List, Union
import json

# Method 1: Generic Dynamic Model
class DynamicJsonModel(BaseModel):
    """A flexible model that can handle any JSON structure"""
    
    class Config:
        extra = "allow"  # Allow any additional fields
        arbitrary_types_allowed = True
    
    def __init__(self, **data):
        # Convert all nested dicts to DynamicJsonModel instances
        for key, value in data.items():
            if isinstance(value, dict):
                data[key] = DynamicJsonModel(**value)
            elif isinstance(value, list):
                data[key] = [DynamicJsonModel(**item) if isinstance(item, dict) else item for item in value]
        super().__init__(**data)

# Method 2: Simple Dynamic Parser (No LangChain dependency - RECOMMENDED)
class SimpleDynamicJsonParser:
    """A simple parser that handles any JSON without LangChain dependencies"""
    
    def parse(self, text: str) -> Dict[str, Any]:
        """Parse JSON string and return dictionary"""
        try:
            # Handle both string representations and actual JSON strings
            if text.startswith("{'") or text.startswith('{"'):
                # Convert Python dict string to proper JSON
                text = text.replace("'", '"')
            return json.loads(text)
        except json.JSONDecodeError as e:
            # Try to evaluate as Python literal
            try:
                import ast
                return ast.literal_eval(text.replace('"', "'"))
            except:
                raise Exception(f"Could not parse JSON: {e}")
    
    def get_format_instructions(self) -> str:
        return """Return a valid JSON object. The JSON should be properly formatted with double quotes around keys and string values."""

# Method 3: Using LangChain's JsonOutputParser (with correct import)
def create_langchain_parser():
    """Create a LangChain JsonOutputParser - requires langchain-core"""
    try:
        # This works with any Pydantic model or without one
        parser = JsonOutputParser()
        return parser
    except ImportError as e:
        print(f"LangChain import error: {e}")
        print("Falling back to SimpleDynamicJsonParser")
        return SimpleDynamicJsonParser()

# Example usage with your data
def demonstrate_parsing():
    # Your sample data
    sample_data = {
        'Product_Name': 'iPhone 14 Pro', 
        'Device_Details': {
            'Display': '6.1 inches Super Retina XDR OLED', 
            'Processor': 'A16 Bionic Chip with 64-bit architecture', 
            'RAM': '6GB', 
            'Storage': '64GB, 256GB, 512GB, 1TB', 
            'Rear_Camera': '48MP main camera, 12MP telephoto camera, 12MP ultra-wide camera', 
            'Front_Camera': '12MP TrueDepth camera', 
            'Battery': 'Up to 23 hours internet use'
        }, 
        'Phone_Price': {
            'Starting_Price': '$999', 
            '64GB_Model': '$999', 
            '256GB_Model': '$1,099', 
            '512GB_Model': '$1,299', 
            '1TB_Model': '$1,499'
        }
    }
    
    print("=== Method 1: SimpleDynamicJsonParser (Recommended - No Dependencies) ===")
    try:
        parser1 = SimpleDynamicJsonParser()
        json_string = str(sample_data)
        parsed1 = parser1.parse(json_string)
        print("Parsed successfully!")
        #print(f"Product Name: {parsed1['Product_Name']}")
        #print(f"Display: {parsed1['Device_Details']['Display']}")
        #print(f"Starting Price: {parsed1['Phone_Price']['Starting_Price']}")
        print(f"Format Instructions: {parser1.get_format_instructions()}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\n=== Method 2: LangChain JsonOutputParser (Correct Import) ===")
    try:
        parser2 = create_langchain_parser()
        json_string = json.dumps(sample_data)
        
        if isinstance(parser2, SimpleDynamicJsonParser):
            parsed2 = parser2.parse(json_string)
        else:
            parsed2 = parser2.parse(json_string)
        
        print("Parsed successfully!")
        print(f"Parser type: {type(parser2)}")
        
        if isinstance(parsed2, dict):
            print(f"Product Name: {parsed2['Product_Name']}")
            print(f"Display: {parsed2['Device_Details']['Display']}")
        else:
            print(f"Parsed data: {parsed2}")
            
    except Exception as e:
        print(f" Error: {e}")

# Utility function for any JSON parsing
def parse_any_json_format(data: Union[str, dict]) -> Dict[str, Any]:
    """
    Universal function to parse any JSON format
    Uses SimpleDynamicJsonParser to avoid import issues
    """
    parser = SimpleDynamicJsonParser()
    
    if isinstance(data, dict):
        return data
    elif isinstance(data, str):
        return parser.parse(data)
    else:
        raise ValueError("Input must be a string or dictionary")

# Pretty print function for nested JSON
def pretty_print_json(data: Dict[str, Any], indent: int = 0) -> None:
    """Recursively print JSON with proper formatting"""
    for key, value in data.items():
        print("  " * indent + f"{key}:")
        if isinstance(value, dict):
            pretty_print_json(value, indent + 1)
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    print("  " * (indent + 1) + f"[{i}]:")
                    pretty_print_json(item, indent + 2)
                else:
                    print("  " * (indent + 1) + f"[{i}]: {item}")
        else:
            print("  " * (indent + 1) + str(value))

if __name__ == "__main__":
    # Run the demonstration
    demonstrate_parsing()
    
    print("\n=== Universal Parser Test ===")
    test_data = {
        'Product_Name': 'iPhone 14 Pro', 
        'Device_Details': '***'
    }
    
    # Test with different input types
    result1 = parse_any_json_format(test_data)  # Dict input
    result2 = parse_any_json_format(str(test_data))  # String input
    
    print(f"Dict input result: {result1['Product_Name']}")
    print(f"String input result: {result2['Product_Name']}")
    
    print("\n=== Pretty Print Example ===")
    pretty_print_json(test_data)
