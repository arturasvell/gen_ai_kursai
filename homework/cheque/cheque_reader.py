from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from rich import print
from dotenv import load_dotenv
import json

class ReceiptItem(BaseModel):
    """
    Represents a single item on the receipt.
    """
    description: str = Field(..., description="Description of the item purchased.")
    quantity: Optional[float] = Field(None, description="Quantity of the item, if specified.")
    unit: Optional[str] = Field(None, description="Unit of measure for the item (e.g., kg).")
    price_per_unit: Optional[float] = Field(None, description="Price per unit of the item.")
    total_item_price: float = Field(..., description="Total price for this specific item.")

class ReceiptInfo(BaseModel):
    """
    Represents extracted information from a receipt.
    """
    company_name: Optional[str] = Field(None, description="The name of the company that issued the receipt.")
    company_address: Optional[str] = Field(None, description="The address of the company.")
    vat_payer_code: Optional[str] = Field(None, description="VAT payer code (PVM moketojo kodas).")
    receipt_id: Optional[str] = Field(None, description="The unique ID or number of the receipt (Kvito Nr.).")
    date: Optional[str] = Field(None, description="The date of the transaction (e.g., YYYY-MM-DD).")
    time: Optional[str] = Field(None, description="The time of the transaction (e.g., HH:MM:SS).")
    store_id: Optional[str] = Field(None, description="The store or branch ID (Pardavėjo ID).")
    cashier_id: Optional[str] = Field(None, description="The cashier or operator ID (Pardavėjas).")
    payment_method: Optional[str] = Field(None, description="Method of payment (e.g., Banko kortele, Debitcard).")
    transaction_id: Optional[str] = Field(None, description="Transaction ID or authorization code (Aut. kodas, Ref. Nr.).")
    total_amount: float = Field(..., description="The total amount of the receipt.")
    total_vat: Optional[float] = Field(None, description="The total VAT (PVM suma) included in the receipt.")
    amount_paid: Optional[float] = Field(None, description="The amount paid by the customer (Mokėti).")
    change_given: Optional[float] = Field(None, description="The amount of change given back (Grąža).")
    items: List[ReceiptItem] = Field([], description="A list of items purchased.")
    additional_info: Optional[str] = Field(None, description="Any other significant text or information on the receipt.")
    fiscal_device_code: Optional[str] = Field(None, description="Fiscal device code (AP-S/N).")
    verification_code: Optional[str] = Field(None, description="VMI verification code (Saugojimo modulis numeris, Kvito parasas, Kvito kodas).")
    payment_card_number_last_digits: Optional[str] = Field(None, description="Last digits of the payment card number.")

load_dotenv()

GOOGLE_AI_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = "gemini-2.5-flash"

client = genai.Client(api_key=GOOGLE_AI_KEY)

cheque_files = ["homework/cheque/data/c2.jpg"]
extracted_cheques_data = []

for cheque_file_path in cheque_files:
    try:
        with open(cheque_file_path, 'rb') as f:
            image_bytes = f.read()

        print(f"\nProcessing {cheque_file_path}...")

        response = client.models.generate_content(
            model=MODEL,
            contents=[
                "Extract the following information from this cheque image: cheque number, date, payee name, numeric amount, amount in words, bank name, account number, routing number, and memo. Return the information in a structured JSON format.",
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type='image/jpeg'
                )
            ],
            config={
                "response_mime_type": "application/json",
                "response_schema": ReceiptInfo
            }
        )

        cheque_data:ReceiptInfo = response.parsed # type: ignore
        extracted_cheques_data.append(cheque_data)
        print(f"Successfully extracted data from {cheque_file_path}")
    except Exception as e:
        print(f"Error processing {cheque_file_path}: {e}")

print("\n--- All Extracted Cheque Data ---")
for i, cheque in enumerate(extracted_cheques_data):
    print(f"Cheque {i+1}:")
    print(cheque.model_dump_json(indent=2))