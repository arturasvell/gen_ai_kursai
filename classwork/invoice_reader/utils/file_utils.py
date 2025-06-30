from pathlib import Path
from typing import List
from rich import print


def find_pdf_files(folder_path: Path) -> List[str]:
    """
    Find all PDF files in the specified folder.
    
    Args:
        folder_path: Path to the folder containing PDF files
        
    Returns:
        List of file paths as strings
        
    Raises:
        SystemExit: If folder doesn't exist or no PDF files found
    """
    PDF_EXTENSIONS = {'.pdf'}
    
    if not folder_path.exists():
        print(f"Error: Folder '{folder_path}' does not exist!")
        raise SystemExit(1)
    
    invoice_files = [
        str(file_path) for file_path in folder_path.iterdir()
        if file_path.is_file() and file_path.suffix.lower() in PDF_EXTENSIONS
    ]
    invoice_files.sort()  # Sort files for consistent ordering
    
    if not invoice_files:
        print(f"No PDF files found in '{folder_path}'")
        raise SystemExit(1)
    
    return invoice_files


def print_found_files(files: List[str], folder_path: Path) -> None:
    """
    Print the list of found PDF files.
    
    Args:
        files: List of file paths
        folder_path: Path to the folder for display purposes
    """
    print(f"Found {len(files)} PDF files in '{folder_path}':")
    for file in files:
        print(f"  - {Path(file).name}")


def ensure_output_directory(output_dir: Path) -> None:
    """
    Create output directory if it doesn't exist.
    
    Args:
        output_dir: Path to the output directory
    """
    output_dir.mkdir(parents=True, exist_ok=True)


def generate_safe_filename(invoice_number: str, index: int, is_valid: bool = True) -> str:
    """
    Generate a safe filename based on invoice number or index.
    
    Args:
        invoice_number: The invoice number
        index: Fallback index if invoice number is invalid
        is_valid: Whether the document is a valid invoice
        
    Returns:
        Safe filename string
    """
    prefix = "invoice" if is_valid else "document"
    
    if invoice_number and invoice_number != "null":
        safe_invoice_number = "".join(c for c in invoice_number if c.isalnum() or c in ('-', '_')).rstrip()
        return f"{prefix}_{safe_invoice_number}.csv"
    else:
        return f"{prefix}_{index+1:03d}.csv" 