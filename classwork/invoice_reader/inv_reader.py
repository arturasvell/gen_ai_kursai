from rich import print
import traceback
from datetime import datetime
from pathlib import Path
import shutil

# Import all utilities from the utils package
from utils import (
    # Configuration
    INVOICE_FOLDER, OUTPUT_DIR, MODEL,
    get_google_ai_client, validate_configuration,
    
    # File operations
    find_pdf_files, print_found_files, ensure_output_directory,
    
    # AI processing
    create_ai_prompt, load_pdfs_to_prompt, process_invoices_with_ai, print_extracted_data,
    
    # CSV export
    create_individual_csv_files, create_items_summary_csv
)


def sort_invoices_by_date(invoices):
    """
    Sort invoices by date, with invalid invoices at the end.
    
    Args:
        invoices: List of InvoiceInfo objects
        
    Returns:
        Sorted list of invoices
    """
    def get_sort_key(invoice):
        if not invoice.is_valid:
            return datetime.max  # Put invalid invoices at the end
        try:
            if invoice.invoice_date:
                return datetime.strptime(invoice.invoice_date, "%Y-%m-%d")
            else:
                return datetime.min  # Put invoices without date at the beginning
        except (ValueError, TypeError):
            return datetime.min
    
    return sorted(invoices, key=get_sort_key)


def create_invalid_documents_csv(invalid_invoices, output_dir):
    """
    Create CSV file for invalid documents.
    
    Args:
        invalid_invoices: List of invalid InvoiceInfo objects
        output_dir: Output directory path
    """
    if not invalid_invoices:
        return
    
    from utils.csv_exporter import get_csv_headers, flatten_invoice_data
    import csv
    
    invalid_csv_file = output_dir / "invalid_documents.csv"
    csv_headers = get_csv_headers()
    
    with open(invalid_csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=csv_headers)
        writer.writeheader()
        
        for invoice in invalid_invoices:
            row = flatten_invoice_data(invoice)
            writer.writerow(row)
    
    print(f"Created invalid documents CSV: {invalid_csv_file}")


def move_processed_files(pdf_files, processed_folder):
    """
    Move processed PDF files to the processed folder.
    
    Args:
        pdf_files: List of PDF file paths
        processed_folder: Path to the processed folder
    """
    # Create processed folder if it doesn't exist
    processed_folder.mkdir(parents=True, exist_ok=True)
    
    moved_count = 0
    for pdf_file in pdf_files:
        source_path = Path(pdf_file)
        if source_path.exists():
            # Generate unique filename to avoid conflicts
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{timestamp}_{source_path.name}"
            destination_path = processed_folder / filename
            
            try:
                shutil.move(str(source_path), str(destination_path))
                moved_count += 1
                print(f"Moved: {source_path.name} -> {destination_path}")
            except Exception as e:
                print(f"Failed to move {source_path.name}: {e}")
    
    print(f"\nMoved {moved_count} files to processed folder: {processed_folder}")


def main():
    """Main function to process and validate PDF documents as invoices."""
    try:
        # Validate configuration
        validate_configuration()
        
        # Get AI client
        client = get_google_ai_client()
        
        # Find PDF files
        pdf_files = find_pdf_files(INVOICE_FOLDER)
        print_found_files(pdf_files, INVOICE_FOLDER)
        
        # Create AI prompt and load PDFs
        prompt = create_ai_prompt()
        load_pdfs_to_prompt(prompt, pdf_files)
        
        # Process PDFs with AI and validate as invoices
        all_invoices = process_invoices_with_ai(client, prompt, MODEL)
        
        # Print extracted data with validation status
        print_extracted_data(all_invoices)
        
        # Ensure output directory exists
        ensure_output_directory(OUTPUT_DIR)
        
        # Sort invoices by date
        sorted_invoices = sort_invoices_by_date(all_invoices.invoices)
        print(f"\nInvoices sorted by date (valid invoices first, then by invoice date)")
        
        # Filter valid and invalid invoices
        valid_invoices = [inv for inv in sorted_invoices if inv.is_valid]
        invalid_invoices = [inv for inv in sorted_invoices if not inv.is_valid]
        
        # Create CSV files for valid invoices
        if valid_invoices:
            from utils.base_models import InvoicesInfo
            valid_invoices_info = InvoicesInfo(invoices=valid_invoices)
            create_individual_csv_files(valid_invoices_info, OUTPUT_DIR)
            create_items_summary_csv(valid_invoices_info, OUTPUT_DIR)
        else:
            print("No valid invoices found. No CSV files created.")
        
        # Create CSV file for invalid documents
        create_invalid_documents_csv(invalid_invoices, OUTPUT_DIR)
        
        # Print summary
        print(f"\n{'='*60}")
        print(f"PROCESSING SUMMARY")
        print(f"{'='*60}")
        print(f"Total documents processed: {len(all_invoices.invoices)}")
        print(f"Valid invoices: {len(valid_invoices)}")
        print(f"Invalid documents: {len(invalid_invoices)}")
        
        # Print excluded documents
        if invalid_invoices:
            print(f"\nThe following documents were excluded because they are not valid invoices:")
            for idx, inv in enumerate(invalid_invoices):
                # Try to print the invoice number if available, otherwise just the index
                doc_id = inv.invoice_number if inv.invoice_number else f"Document #{idx+1}"
                print(f"  - {doc_id}")
        
        # Move processed files to processed folder
        processed_folder = INVOICE_FOLDER / "processed"
        move_processed_files(pdf_files, processed_folder)
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()