import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai


# Load environment variables
load_dotenv()

# Configuration constants
GOOGLE_AI_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = "gemini-1.5-flash"

# Paths
INVOICE_FOLDER = Path("classwork/invoice_reader/invoices")
OUTPUT_DIR = Path("classwork/invoice_reader/results")


def get_google_ai_client():
    """
    Get configured Google AI client.
    
    Returns:
        Configured genai.Client instance
        
    Raises:
        ValueError: If API key is not configured
    """
    if not GOOGLE_AI_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    return genai.Client(api_key=GOOGLE_AI_KEY)


def validate_configuration():
    """
    Validate that all required configuration is present.
    
    Raises:
        ValueError: If required configuration is missing
    """
    if not GOOGLE_AI_KEY:
        raise ValueError("GOOGLE_API_KEY environment variable is not set")
    
    if not INVOICE_FOLDER.exists():
        raise ValueError(f"Invoice folder does not exist: {INVOICE_FOLDER}") 