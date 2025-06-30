from rich import print
import traceback

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
        
        # Filter only valid invoices
        from utils.base_models import InvoicesInfo
        valid_invoices = [inv for inv in all_invoices.invoices if inv.is_valid]
        invalid_invoices = [inv for inv in all_invoices.invoices if not inv.is_valid]
        if valid_invoices:
            valid_invoices_info = InvoicesInfo(invoices=valid_invoices)
            create_individual_csv_files(valid_invoices_info, OUTPUT_DIR)
            create_items_summary_csv(valid_invoices_info, OUTPUT_DIR)
        else:
            print("No valid invoices found. No CSV files created.")
        
        # Print excluded documents
        if invalid_invoices:
            print("\nThe following documents were excluded because they are not valid invoices:")
            for idx, inv in enumerate(invalid_invoices):
                # Try to print the invoice number if available, otherwise just the index
                doc_id = inv.invoice_number if inv.invoice_number else f"Document #{idx+1}"
                print(f"  - {doc_id}")
        
    except Exception as e:
        print(f"\nAn error occurred: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()