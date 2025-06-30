import csv
import json
from pathlib import Path
from typing import Dict, Any, List
from rich import print
from utils.base_models import InvoicesInfo, InvoiceInfo


def get_csv_headers() -> List[str]:
    """
    Get the list of CSV headers for invoice data.
    
    Returns:
        List of header strings
    """
    return [
        'is_valid', 'invoice_number', 'invoice_date', 'due_date',
        'seller_name', 'seller_street', 'seller_city', 'seller_state', 'seller_postal_code', 'seller_country', 'seller_email', 'seller_phone',
        'buyer_name', 'buyer_street', 'buyer_city', 'buyer_state', 'buyer_postal_code', 'buyer_country', 'buyer_email', 'buyer_phone',
        'customer_id', 'po_number', 'salesperson', 'shipped_via', 'terms', 'service_period',
        'subtotal', 'tax_rate', 'tax_amount', 'discount_amount', 'other_charges', 'total_amount',
        'previous_balance', 'amount_due', 'notes',
        'ship_to_name', 'ship_to_street', 'ship_to_city', 'ship_to_state', 'ship_to_postal_code',
        'service_address_name', 'service_address_street', 'service_address_city', 'service_address_state', 'service_address_postal_code',
        'remit_to_name', 'remit_to_street', 'remit_to_city', 'remit_to_state', 'remit_to_postal_code',
        'items_count', 'items_details'
    ]


def flatten_invoice_data(invoice: InvoiceInfo) -> Dict[str, Any]:
    """
    Flatten invoice data for CSV export.
    
    Args:
        invoice: InvoiceInfo object to flatten
        
    Returns:
        Dictionary with flattened invoice data
    """
    row = {
        'is_valid': invoice.is_valid,
        'invoice_number': invoice.invoice_number,
        'invoice_date': invoice.invoice_date,
        'due_date': invoice.due_date,
        'seller_name': invoice.seller_name,
        'customer_id': invoice.customer_id,
        'po_number': invoice.po_number,
        'salesperson': invoice.salesperson,
        'shipped_via': invoice.shipped_via,
        'terms': invoice.terms,
        'service_period': invoice.service_period,
        'subtotal': invoice.subtotal,
        'tax_rate': invoice.tax_rate,
        'tax_amount': invoice.tax_amount,
        'discount_amount': invoice.discount_amount,
        'other_charges': invoice.other_charges,
        'total_amount': invoice.total_amount,
        'previous_balance': invoice.previous_balance,
        'amount_due': invoice.amount_due,
        'notes': invoice.notes,
        'items_count': len(invoice.items)
    }
    
    # Handle seller address
    if invoice.seller_address:
        row.update({
            'seller_street': invoice.seller_address.street,
            'seller_city': invoice.seller_address.city,
            'seller_state': invoice.seller_address.state,
            'seller_postal_code': invoice.seller_address.postal_code,
            'seller_country': invoice.seller_address.country,
            'seller_email': invoice.seller_address.email,
            'seller_phone': invoice.seller_address.phone
        })
    
    # Handle buyer address
    if invoice.buyer_address:
        row.update({
            'buyer_name': invoice.buyer_address.name or invoice.buyer_name,
            'buyer_street': invoice.buyer_address.street,
            'buyer_city': invoice.buyer_address.city,
            'buyer_state': invoice.buyer_address.state,
            'buyer_postal_code': invoice.buyer_address.postal_code,
            'buyer_country': invoice.buyer_address.country,
            'buyer_email': invoice.buyer_address.email,
            'buyer_phone': invoice.buyer_address.phone
        })
    else:
        row['buyer_name'] = invoice.buyer_name
    
    # Handle ship_to address
    if invoice.ship_to_address:
        row.update({
            'ship_to_name': invoice.ship_to_address.name,
            'ship_to_street': invoice.ship_to_address.street,
            'ship_to_city': invoice.ship_to_address.city,
            'ship_to_state': invoice.ship_to_address.state,
            'ship_to_postal_code': invoice.ship_to_address.postal_code
        })
    
    # Handle service address
    if invoice.service_address:
        row.update({
            'service_address_name': invoice.service_address.name,
            'service_address_street': invoice.service_address.street,
            'service_address_city': invoice.service_address.city,
            'service_address_state': invoice.service_address.state,
            'service_address_postal_code': invoice.service_address.postal_code
        })
    
    # Handle remit_to address
    if invoice.remit_to_address:
        row.update({
            'remit_to_name': invoice.remit_to_address.name,
            'remit_to_street': invoice.remit_to_address.street,
            'remit_to_city': invoice.remit_to_address.city,
            'remit_to_state': invoice.remit_to_address.state,
            'remit_to_postal_code': invoice.remit_to_address.postal_code
        })
    
    # Create a JSON string of items for detailed information
    items_details = []
    for item in invoice.items:
        item_dict = {
            'code': item.item_code,
            'description': item.description,
            'qty': item.quantity,
            'unit': item.unit,
            'unit_price': item.unit_price,
            'discount': item.discount,
            'tax': item.tax,
            'total': item.total_price
        }
        items_details.append(item_dict)
    row['items_details'] = json.dumps(items_details, ensure_ascii=False)
    
    return row


def create_individual_csv_files(all_invoices: InvoicesInfo, output_dir: Path) -> None:
    """
    Create separate CSV files for each invoice.
    
    Args:
        all_invoices: InvoicesInfo object containing all invoices
        output_dir: Directory to save CSV files
    """
    from utils.file_utils import generate_safe_filename
    
    csv_headers = get_csv_headers()
    
    for i, invoice in enumerate(all_invoices.invoices):
        csv_filename = generate_safe_filename(invoice.invoice_number, i, invoice.is_valid)
        csv_file = output_dir / csv_filename
        
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=csv_headers)
            writer.writeheader()
            
            row = flatten_invoice_data(invoice)
            writer.writerow(row)
        
        validity_status = "VALID" if invoice.is_valid else "INVALID"
        print(f"Created CSV for PDF {invoice.invoice_number} ({validity_status}): {csv_file}")
    
    valid_count = sum(1 for invoice in all_invoices.invoices if invoice.is_valid)
    invalid_count = len(all_invoices.invoices) - valid_count
    print(f"\nCreated {len(all_invoices.invoices)} separate CSV files in: {output_dir}")
    print(f"Valid invoices: {valid_count}, Invalid documents: {invalid_count}")


def create_items_summary_csv(all_invoices: InvoicesInfo, output_dir: Path) -> None:
    """
    Create a summary CSV file containing all invoice items.
    
    Args:
        all_invoices: InvoicesInfo object containing all invoices
        output_dir: Directory to save the CSV file
    """
    items_csv_file = output_dir / "invoice_items.csv"
    items_headers = [
        'is_valid', 'invoice_number', 'item_code', 'description', 'quantity', 'unit', 
        'unit_price', 'discount', 'tax', 'total_price'
    ]
    
    with open(items_csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=items_headers)
        writer.writeheader()
        
        for invoice in all_invoices.invoices:
            for item in invoice.items:
                writer.writerow({
                    'is_valid': invoice.is_valid,
                    'invoice_number': invoice.invoice_number,
                    'item_code': item.item_code,
                    'description': item.description,
                    'quantity': item.quantity,
                    'unit': item.unit,
                    'unit_price': item.unit_price,
                    'discount': item.discount,
                    'tax': item.tax,
                    'total_price': item.total_price
                })
    
    print(f"Invoice items summary saved to CSV: {items_csv_file}") 