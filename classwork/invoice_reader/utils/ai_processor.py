from google import genai
from google.genai import types
from typing import List
from rich import print
from utils.base_models import InvoicesInfo


def create_ai_prompt() -> List:
    """
    Create the base prompt for invoice processing.
    
    Returns:
        List containing the prompt text
    """
    return [
        "For each of the following PDFs, first determine if it has the typical structure of an invoice. "
        "A valid invoice should have features such as: an invoice number, billing and seller details, a table of line items, and totals. "
        "If the PDF does NOT have this structure (for example, if it is a novel, a letter, or any document without these invoice-like fields and tables), set is_valid to false and provide minimal placeholder data for required fields. "
        "If it DOES have the structure of an invoice, set is_valid to true and extract all information according to the provided JSON schema. "
        "The actual content or plausibility of the items is not relevant—only the format/structure matters. "
        "Return the information as a list of structured JSON objects, one for each PDF."
    ]


def load_pdfs_to_prompt(prompt: List, invoice_files: List[str]) -> None:
    """
    Load PDF files into the prompt for AI processing.
    
    Args:
        prompt: The prompt list to append PDF data to
        invoice_files: List of PDF file paths
    """
    print(f"\nLoading {len(invoice_files)} PDFs...")
    for invoice_file_path in invoice_files:
        with open(invoice_file_path, 'rb') as f:
            prompt.append(types.Part.from_bytes(
                data=f.read(),
                mime_type='application/pdf'
            )) # type: ignore


def process_invoices_with_ai(client: genai.Client, prompt: List, model: str) -> InvoicesInfo:
    """
    Process invoices using Google AI API.
    
    Args:
        client: Google AI client instance
        prompt: List containing prompt and PDF data
        model: Model name to use for processing
        
    Returns:
        InvoicesInfo object containing extracted invoice data
    """
    print(f"\nProcessing {len(prompt) - 1} PDFs in a single batch...")
    
    response = client.models.generate_content(
        model=f"models/{model}",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": InvoicesInfo
        }
    )
    
    all_invoices: InvoicesInfo = response.parsed # type: ignore
    print(f"\nSuccessfully extracted data from {len(all_invoices.invoices)} PDFs.")
    
    return all_invoices


def print_extracted_data(all_invoices: InvoicesInfo) -> None:
    """
    Print the extracted invoice data in a formatted way.
    
    Args:
        all_invoices: InvoicesInfo object containing extracted data
    """
    print("\n--- All Extracted PDF Data ---")
    for i, invoice in enumerate(all_invoices.invoices):
        print(f"\n{'='*50}")
        validity_status = "VALID INVOICE" if invoice.is_valid else "INVALID (Not an invoice)"
        print(f"PDF {i+1}: {invoice.invoice_number} - {validity_status}")
        print(f"{'='*50}")
        print(invoice.model_dump_json(indent=2)) 