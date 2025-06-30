from pydantic import BaseModel, Field
from typing import Optional, List

class InvoiceItem(BaseModel):
    item_code: Optional[str] = Field(None, description="Item code or SKU")
    description: str = Field(..., description="Description of the item or service")
    quantity: Optional[float] = Field(None, description="Quantity of the item")
    unit: Optional[str] = Field(None, description="Unit of measure (e.g., units, hours, pages)")
    unit_price: Optional[float] = Field(None, description="Price per unit")
    discount: Optional[float] = Field(None, description="Discount amount or percentage")
    tax: Optional[float] = Field(None, description="Tax amount for this item")
    total_price: float = Field(..., description="Total price for this line item")

class Address(BaseModel):
    name: Optional[str] = Field(None, description="Company or person name")
    street: Optional[str] = Field(None, description="Street address")
    city: Optional[str] = Field(None, description="City")
    state: Optional[str] = Field(None, description="State or province")
    postal_code: Optional[str] = Field(None, description="ZIP or postal code")
    country: Optional[str] = Field(None, description="Country")
    email: Optional[str] = Field(None, description="Email address")
    phone: Optional[str] = Field(None, description="Phone number")

class InvoiceInfo(BaseModel):
    is_valid: bool = Field(..., description="Whether this PDF is actually a valid invoice document (not a novel, receipt, or other document)")
    invoice_number: str = Field(..., description="Invoice number or ID")
    invoice_date: Optional[str] = Field(None, description="Invoice date (YYYY-MM-DD format)")
    due_date: Optional[str] = Field(None, description="Payment due date (YYYY-MM-DD format)")
    
    # Seller information
    seller_name: Optional[str] = Field(None, description="Name of the selling company")
    seller_address: Optional[Address] = Field(None, description="Seller's address details")
    
    # Buyer information
    buyer_name: Optional[str] = Field(None, description="Name of the buyer/customer")
    buyer_address: Optional[Address] = Field(None, description="Buyer's billing address")
    customer_id: Optional[str] = Field(None, description="Customer ID or account number")
    
    # Additional addresses
    ship_to_address: Optional[Address] = Field(None, description="Shipping address if different from billing")
    service_address: Optional[Address] = Field(None, description="Service address if applicable")
    
    # Order details
    po_number: Optional[str] = Field(None, description="Purchase order number")
    salesperson: Optional[str] = Field(None, description="Salesperson name")
    shipped_via: Optional[str] = Field(None, description="Shipping method")
    terms: Optional[str] = Field(None, description="Payment terms")
    service_period: Optional[str] = Field(None, description="Service period covered")
    
    # Line items
    items: List[InvoiceItem] = Field([], description="List of items/services on the invoice")
    
    # Totals
    subtotal: float = Field(..., description="Subtotal before tax and other charges")
    tax_rate: Optional[float] = Field(None, description="Tax rate percentage")
    tax_amount: Optional[float] = Field(None, description="Total tax amount")
    discount_amount: Optional[float] = Field(None, description="Total discount amount")
    other_charges: Optional[float] = Field(None, description="Other charges or fees")
    total_amount: float = Field(..., description="Total invoice amount")
    
    # Payment information
    previous_balance: Optional[float] = Field(None, description="Previous unpaid balance")
    amount_due: Optional[float] = Field(None, description="Total amount due including previous balance")
    
    # Additional information
    notes: Optional[str] = Field(None, description="Additional notes or terms")
    remit_to_address: Optional[Address] = Field(None, description="Remittance address")

class InvoicesInfo(BaseModel):
    invoices: List[InvoiceInfo] = Field(..., description="List of extracted invoice information objects")