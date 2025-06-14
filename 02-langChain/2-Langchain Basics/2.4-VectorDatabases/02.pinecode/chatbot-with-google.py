import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
loaded = load_dotenv()

print(f".env file loaded: {loaded}") # Should print True if .env was found

# Get the API key from the environment variable
g_api_key = "AIzaSyAiZR1HLn9qaSXx6xDkBl0pxcKl_H6r0kY"
print(f"API Key from env: '{g_api_key}'") # Check if this prints your key or None


if not g_api_key:
    print("ERROR: GOOGLE_API_KEY not found or is empty in environment variables.")
    print("Please ensure your .env file is correctly formatted and in the project root:")
    print("GOOGLE_API_KEY=\"YOUR_API_KEY_HERE\"")
    raise ValueError("GOOGLE_API_KEY not found. Make sure it's set in your .env file.")
else:
    print(f"Successfully loaded API key starting with: {g_api_key[:5]}... and ending with: ...{g_api_key[-5:]}")


# Configure the generative AI SDK with the API key
genai.configure(api_key=g_api_key)
genai

# --- Example: Using the Gemini Pro model ---
try:
    # Choose a model (e.g., 'gemini-pro' for text, 'gemini-pro-vision' for multimodal)
    model = genai.GenerativeModel("gemini-1.5-flash-latest")

    prompt = "Write a short story about a robot who discovers music."
    print(f"Sending prompt: {prompt}\n")

    response = model.generate_content(prompt)

    print("--- Response ---")
    print(response.text)
    print("----------------")

    # If you need to see parts (e.g., for safety ratings or multiple candidates)
    # print(response.parts)
    # print(response.candidates)

except Exception as e:
    print(f"An error occurred: {e}")
    # You might want to inspect response.prompt_feedback for safety issues
    # if 'response' in locals() and response.prompt_feedback:
    # print(f"Prompt Feedback: {response.prompt_feedback}")

# --- Example: Listing available models ---
# print("\n--- Available Models ---")
# for m in genai.list_models():
# if 'generateContent' in m.supported_generation_methods:
# print(m.name)
# print("----------------------")