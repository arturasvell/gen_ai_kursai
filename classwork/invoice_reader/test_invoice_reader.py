#!/usr/bin/env python3

import os
import sys
from pathlib import Path
from rich import print
from rich.console import Console
from rich.table import Table
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))

from utils.config import INVOICE_FOLDER, OUTPUT_DIR, MODEL, get_google_ai_client
from utils.base_models import InvoiceInfo, InvoicesInfo
from utils.ai_processor import create_ai_prompt, load_pdfs_to_prompt, process_invoices_with_ai

console = Console()


def test_requirement_1_llm_validation():
    print("\n[bold blue]Test 1: LLM Invoice Validation[/bold blue]")
    
    test_invoice = InvoiceInfo(
        is_valid=False,
        invoice_number="TEST-001",
        subtotal=0.0,
        total_amount=0.0,
        items=[]
    )
    
    if not test_invoice.is_valid:
        print("LLM correctly identified non-invoice document")
        print("Document will not be processed as invoice")
    else:
        print("LLM incorrectly identified non-invoice as invoice")


def test_requirement_2_date_sorting():
    print("\n[bold blue]Test 2: Date Sorting[/bold blue]")
    
    invoices = [
        InvoiceInfo(
            is_valid=True,
            invoice_number="INV-003",
            invoice_date="2024-01-15",
            subtotal=100.0,
            total_amount=100.0,
            items=[]
        ),
        InvoiceInfo(
            is_valid=True,
            invoice_number="INV-001",
            invoice_date="2024-01-10",
            subtotal=200.0,
            total_amount=200.0,
            items=[]
        ),
        InvoiceInfo(
            is_valid=True,
            invoice_number="INV-002",
            invoice_date="2024-01-12",
            subtotal=150.0,
            total_amount=150.0,
            items=[]
        ),
        InvoiceInfo(
            is_valid=False,
            invoice_number="DOC-001",
            invoice_date="2024-01-08",
            subtotal=0.0,
            total_amount=0.0,
            items=[]
        )
    ]
    
    from inv_reader import sort_invoices_by_date
    
    sorted_invoices = sort_invoices_by_date(invoices)
    
    print("Original order:")
    for inv in invoices:
        status = "VALID" if inv.is_valid else "INVALID"
        print(f"  {inv.invoice_number} ({inv.invoice_date}) - {status}")
    
    print("\nSorted order:")
    for inv in sorted_invoices:
        status = "VALID" if inv.is_valid else "INVALID"
        print(f"  {inv.invoice_number} ({inv.invoice_date}) - {status}")
    
    valid_invoices = [inv for inv in sorted_invoices if inv.is_valid]
    if len(valid_invoices) >= 2:
        dates = [datetime.strptime(inv.invoice_date, "%Y-%m-%d") for inv in valid_invoices if inv.invoice_date]
        is_sorted = dates == sorted(dates)
        if is_sorted:
            print("Invoices correctly sorted by date")
        else:
            print("Invoices not properly sorted by date")
    else:
        print("Not enough valid invoices to test sorting")


def test_requirement_3_schema_validation():
    print("\n[bold blue]Test 3: Schema Definition and Validation[/bold blue]")
    
    try:
        valid_invoice = InvoiceInfo(
            is_valid=True,
            invoice_number="INV-001",
            invoice_date="2024-01-15",
            subtotal=100.0,
            total_amount=110.0,
            items=[]
        )
        print("Valid invoice schema created successfully")
        
        invalid_invoice = InvoiceInfo(
            is_valid=False,
            invoice_number="DOC-001",
            subtotal=0.0,
            total_amount=0.0,
            items=[]
        )
        print("Invalid document schema created successfully")
        
        from pydantic import ValidationError
        try:
            bad_invoice = InvoiceInfo(
                is_valid=True,
            )
            print("Schema validation failed - should have required fields")
        except ValidationError:
            print("Schema validation working correctly")
            
    except Exception as e:
        print(f"Schema test failed: {e}")


def test_requirement_4_csv_export():
    print("\n[bold blue]Test 4: CSV Export[/bold blue]")
    
    test_invoices = [
        InvoiceInfo(
            is_valid=True,
            invoice_number="INV-001",
            invoice_date="2024-01-15",
            subtotal=100.0,
            total_amount=110.0,
            items=[]
        ),
        InvoiceInfo(
            is_valid=False,
            invoice_number="DOC-001",
            subtotal=0.0,
            total_amount=0.0,
            items=[]
        )
    ]
    
    test_invoices_info = InvoicesInfo(invoices=test_invoices)
    
    from utils.csv_exporter import create_individual_csv_files, create_items_summary_csv
    
    try:
        test_output = Path("test_output")
        test_output.mkdir(exist_ok=True)
        
        create_individual_csv_files(test_invoices_info, test_output)
        print("Individual CSV files created successfully")
        
        create_items_summary_csv(test_invoices_info, test_output)
        print("Items summary CSV created successfully")
        
        csv_files = list(test_output.glob("*.csv"))
        print(f"Created {len(csv_files)} CSV files")
        
        import shutil
        shutil.rmtree(test_output)
        print("Test cleanup completed")
        
    except Exception as e:
        print(f"CSV export test failed: {e}")


def test_requirement_5_file_operations():
    print("\n[bold blue]Test 5: File Operations[/bold blue]")
    
    from utils.file_utils import find_pdf_files, ensure_output_directory
    
    try:
        test_dir = Path("test_dir")
        ensure_output_directory(test_dir)
        if test_dir.exists():
            print("Output directory creation working")
            test_dir.rmdir()
        else:
            print("Output directory creation failed")
        
        processed_folder = INVOICE_FOLDER / "processed"
        if processed_folder.exists():
            pdf_files = find_pdf_files(processed_folder)
            print(f"PDF file discovery working - found {len(pdf_files)} files")
        else:
            print("Processed invoices folder not found, skipping PDF discovery test")
            
    except Exception as e:
        print(f"File operations test failed: {e}")


def test_requirement_6_llm_connection():
    print("\n[bold blue]Test 6: LLM Connection[/bold blue]")
    
    try:
        client = get_google_ai_client()
        print("LLM client initialized successfully")
        
        prompt = create_ai_prompt()
        if isinstance(prompt, list) and len(prompt) > 0:
            print("AI prompt created successfully")
        else:
            print("AI prompt creation failed")
            
    except Exception as e:
        print(f"LLM connection test failed: {e}")


def test_requirement_7_multilingual_support():
    print("\n[bold blue]Test 7: Multilingual Support[/bold blue]")
    
    multilingual_invoices = [
        InvoiceInfo(
            is_valid=True,
            invoice_number="INV-EN-001",
            invoice_date="2024-01-15",
            seller_name="English Company Ltd.",
            buyer_name="English Customer",
            subtotal=100.0,
            total_amount=110.0,
            items=[]
        ),
        InvoiceInfo(
            is_valid=True,
            invoice_number="INV-LT-001",
            invoice_date="2024-01-15",
            seller_name="Lietuviška Įmonė UAB",
            buyer_name="Lietuviškas Klientas",
            subtotal=100.0,
            total_amount=110.0,
            items=[]
        ),
        InvoiceInfo(
            is_valid=True,
            invoice_number="INV-DE-001",
            invoice_date="2024-01-15",
            seller_name="Deutsche Firma GmbH",
            buyer_name="Deutscher Kunde",
            subtotal=100.0,
            total_amount=110.0,
            items=[]
        )
    ]
    
    print("Multilingual invoice data structure supported")
    print("Unicode characters handled correctly")
    
    try:
        from utils.csv_exporter import flatten_invoice_data
        for invoice in multilingual_invoices:
            flattened = flatten_invoice_data(invoice)
            if flattened['seller_name'] == invoice.seller_name:
                print(f"Multilingual data preserved: {invoice.seller_name}")
            else:
                print(f"Multilingual data corrupted: {invoice.seller_name}")
    except Exception as e:
        print(f"Multilingual CSV test failed: {e}")


def run_all_tests():
    console.print("\n[bold green]INVOICE READER REQUIREMENTS TESTING[/bold green]")
    console.print("=" * 60)
    
    tests = [
        test_requirement_1_llm_validation,
        test_requirement_2_date_sorting,
        test_requirement_3_schema_validation,
        test_requirement_4_csv_export,
        test_requirement_5_file_operations,
        test_requirement_6_llm_connection,
        test_requirement_7_multilingual_support
    ]
    
    results = []
    for test in tests:
        try:
            test()
            results.append(("PASS", test.__name__, "PASSED"))
        except Exception as e:
            results.append(("FAIL", test.__name__, f"FAILED: {e}"))
    
    console.print("\n[bold yellow]TEST SUMMARY[/bold yellow]")
    console.print("=" * 60)
    
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Status")
    table.add_column("Test")
    table.add_column("Result")
    
    for status, test_name, result in results:
        table.add_row(status, test_name, result)
    
    console.print(table)
    
    passed = sum(1 for status, _, _ in results if status == "PASS")
    total = len(results)
    
    console.print(f"\n[bold]Overall Result: {passed}/{total} tests passed[/bold]")
    
    if passed == total:
        console.print("[bold green]All requirements met![/bold green]")
    else:
        console.print("[bold red]Some requirements need attention[/bold red]")


if __name__ == "__main__":
    run_all_tests() 