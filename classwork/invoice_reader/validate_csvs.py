import csv
import json
from pathlib import Path
import os

def validate_csv_files():
    """Validate the generated CSV files for data quality and consistency."""
    
    # Use path relative to this script's location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    results_dir = Path(os.path.join(script_dir, "results"))
    csv_files = list(results_dir.glob("invoice_*.csv"))
    
    print(f"Found {len(csv_files)} CSV files to validate:")
    for file in csv_files:
        print(f"  - {file.name}")
    
    print("\n" + "="*60)
    print("VALIDATION RESULTS")
    print("="*60)
    
    total_issues = 0
    
    for csv_file in csv_files:
        print(f"\n📄 Validating: {csv_file.name}")
        issues = []
        
        try:
            # Read CSV file
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
            
            if len(rows) == 0:
                issues.append("❌ Empty CSV file")
                continue
            
            # Get the single row (each CSV should have one invoice)
            row = rows[0]
            
            # Basic structure validation
            required_columns = [
                'invoice_number', 'invoice_date', 'seller_name', 'buyer_name',
                'subtotal', 'total_amount', 'items_count', 'items_details'
            ]
            
            missing_columns = [col for col in required_columns if col not in row]
            if missing_columns:
                issues.append(f"❌ Missing required columns: {missing_columns}")
            
            # Data type validation
            if not row['invoice_number'] or row['invoice_number'] == 'null':
                issues.append("⚠️  Invoice number is null or missing")
            
            if not row['invoice_date']:
                issues.append("⚠️  Invoice date is missing")
            
            if not row['seller_name']:
                issues.append("⚠️  Seller name is missing")
            
            if not row['buyer_name']:
                issues.append("⚠️  Buyer name is missing")
            
            # Numeric validation
            try:
                subtotal = float(row['subtotal']) if row['subtotal'] else 0
                total_amount = float(row['total_amount']) if row['total_amount'] else 0
                
                if subtotal < 0:
                    issues.append("❌ Negative subtotal")
                if total_amount < 0:
                    issues.append("❌ Negative total amount")
                    
            except (ValueError, TypeError):
                issues.append("❌ Invalid numeric values for amounts")
            
            # Items validation
            try:
                items_count = int(row['items_count']) if row['items_count'] else 0
                items_details = row['items_details']
                
                if items_details:
                    items_json = json.loads(items_details)
                    actual_items_count = len(items_json)
                    
                    if items_count != actual_items_count:
                        issues.append(f"⚠️  Items count mismatch: declared {items_count}, actual {actual_items_count}")
                    
                    # Validate each item
                    for i, item in enumerate(items_json):
                        if 'code' not in item:
                            issues.append(f"⚠️  Item {i+1} missing code")
                        if 'description' not in item:
                            issues.append(f"⚠️  Item {i+1} missing description")
                        if 'qty' not in item:
                            issues.append(f"⚠️  Item {i+1} missing quantity")
                        if 'total' not in item:
                            issues.append(f"⚠️  Item {i+1} missing total price")
                            
                else:
                    issues.append("⚠️  Items details are missing")
                    
            except (json.JSONDecodeError, KeyError, TypeError) as e:
                issues.append(f"❌ Invalid items JSON: {str(e)}")
            
            # Address validation
            address_fields = ['seller_street', 'seller_city', 'buyer_street', 'buyer_city']
            for field in address_fields:
                if field in row and row[field]:
                    if len(str(row[field]).strip()) < 2:
                        issues.append(f"⚠️  Very short {field}: '{row[field]}'")
            
            # Print results
            if issues:
                for issue in issues:
                    print(f"  {issue}")
                total_issues += len(issues)
            else:
                print("  ✅ All validations passed")
                
            # Print summary stats
            print(f"  📊 Invoice: {row['invoice_number']}")
            print(f"  📅 Date: {row['invoice_date']}")
            print(f"  💰 Total: ${total_amount:.2f}")
            print(f"  📦 Items: {items_count}")
            
        except Exception as e:
            print(f"  ❌ Error reading file: {str(e)}")
            total_issues += 1
    
    print(f"\n" + "="*60)
    print(f"SUMMARY: {total_issues} total issues found")
    print("="*60)
    
    if total_issues == 0:
        print("🎉 All CSV files passed validation!")
    else:
        print("⚠️  Some issues were found. Please review the details above.")

if __name__ == "__main__":
    validate_csv_files() 