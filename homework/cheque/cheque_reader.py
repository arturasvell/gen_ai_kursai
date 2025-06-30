from google import genai
from google.genai import types
from pydantic import BaseModel, Field
from typing import Optional, List
import os
from rich import print
from dotenv import load_dotenv
import json

# --- Pydantic Schemas ---

class ReceiptItem(BaseModel):
    description: str = Field(..., description="Description of the item purchased. Could be something generic like Prekė.")
    quantity: Optional[float] = Field(None, description="Quantity of the item, if specified.")
    unit: Optional[str] = Field(None, description="Unit of measure for the item (e.g., kg).")
    price_per_unit: Optional[float] = Field(None, description="Price per unit of the item.")
    total_item_price: float = Field(..., description="Total price for this specific item.")

class ReceiptInfo(BaseModel):
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
    items: list[ReceiptItem] = Field([], description="A list of items purchased.")
    additional_info: Optional[str] = Field(None, description="Any other significant text or information on the receipt.")
    fiscal_device_code: Optional[str] = Field(None, description="Fiscal device code (AP-S/N).")
    verification_code: Optional[str] = Field(None, description="VMI verification code (Saugojimo modulis numeris, Kvito parasas, Kvito kodas).")
    payment_card_number_last_digits: Optional[str] = Field(None, description="Last digits of the payment card number.")

class ReceiptsInfo(BaseModel):
    receipts: list[ReceiptInfo] = Field(..., description="A list of extracted receipt information objects.")


load_dotenv()

GOOGLE_AI_KEY = os.getenv("GOOGLE_API_KEY")
MODEL = "gemini-1.5-flash"

client = genai.Client(api_key=GOOGLE_AI_KEY)

receipt_files = [
    "homework/cheque/data/c7.jpg",
    "homework/cheque/data/c1.jpg",
    "homework/cheque/data/c2.jpg",
    "homework/cheque/data/c3.jpg",
    "homework/cheque/data/c4.jpg",
    "homework/cheque/data/c5.jpg",
    "homework/cheque/data/c6.jpg"
]

prompt = [
    "For each of the following receipt images, extract the information according to the provided JSON schema. "
    "Return the information as a list of structured JSON objects, one for each receipt."
]

try:
    print(f"Loading {len(receipt_files)} images...")
    for receipt_file_path in receipt_files:
        with open(receipt_file_path, 'rb') as f:
            prompt.append(types.Part.from_bytes(
                data=f.read(),
                mime_type='image/jpeg'
            )) # type: ignore

    print(f"\nProcessing {len(receipt_files)} images in a single batch...")

    response = client.models.generate_content(
        model=f"models/{MODEL}",
        contents=prompt,
        config={
            "response_mime_type": "application/json",
            "response_schema": ReceiptsInfo
        }
    )

    all_receipts: ReceiptsInfo = response.parsed # type: ignore

    print(f"Successfully extracted data from {len(all_receipts.receipts)} images.")

    print("\n--- All Extracted Receipt Data ---")
    for i, receipt in enumerate(all_receipts.receipts):
        print(f"Receipt {i+1}:")
        print(receipt.model_dump_json(indent=2))

except Exception as e:
    print(f"An error occurred: {e}")