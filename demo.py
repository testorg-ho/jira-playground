#!/usr/bin/env python3
"""
Demo script for Jira CSV Manager functionality.

This script demonstrates how the CSV management works without requiring actual Jira credentials.
It simulates downloading, modifying, and uploading CSV files.
"""

import csv
import io
import tempfile
import os
from typing import List, Optional


def simulate_csv_download(ticket_id: str, has_existing_csv: bool = True) -> Optional[List[List[str]]]:
    """
    Simulate downloading CSV from Jira ticket.
    
    Args:
        ticket_id: The ticket ID
        has_existing_csv: Whether to simulate existing CSV or not
        
    Returns:
        Simulated CSV rows or None
    """
    print(f"🔍 Checking ticket {ticket_id} for existing items.csv...")
    
    if has_existing_csv:
        # Simulate existing CSV data
        existing_data = [
            ['Number', 'Item Name'],
            ['1', 'Existing Product A'],
            ['2', 'Existing Product B'],
            ['5', 'Existing Product E']  # Gap in numbering to test logic
        ]
        print(f"✅ Found existing items.csv with {len(existing_data)-1} products")
        return existing_data
    else:
        print("ℹ️  No existing items.csv found - will create new one")
        return None


def create_csv_content(existing_rows: Optional[List[List[str]]], products: List[str]) -> str:
    """
    Create CSV content with existing data and new products.
    
    Args:
        existing_rows: Existing CSV rows (including header) or None
        products: List of products to add
        
    Returns:
        CSV content as string
    """
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Handle header
    if existing_rows and len(existing_rows) > 0:
        # Use existing header
        header = existing_rows[0]
        writer.writerow(header)
        
        # Write existing data rows (skip header)
        for row in existing_rows[1:]:
            writer.writerow(row)
        
        # Find the next number to use
        next_number = 1
        for row in existing_rows[1:]:
            if len(row) > 0 and row[0].isdigit():
                next_number = max(next_number, int(row[0]) + 1)
    else:
        # Create new header
        header = ['Number', 'Item Name']
        writer.writerow(header)
        next_number = 1
    
    # Add new products
    for product in products:
        writer.writerow([str(next_number), product])
        next_number += 1
    
    csv_content = output.getvalue()
    output.close()
    
    return csv_content


def simulate_csv_upload(ticket_id: str, csv_content: str) -> None:
    """
    Simulate uploading CSV to Jira ticket.
    
    Args:
        ticket_id: The ticket ID
        csv_content: CSV content to upload
    """
    print(f"🔄 Removing any existing items.csv from {ticket_id}...")
    print(f"📤 Uploading new items.csv to {ticket_id}...")
    
    # Save to temporary file to show the result
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
        temp_file.write(csv_content)
        temp_file_path = temp_file.name
    
    print(f"✅ Successfully uploaded items.csv")
    print(f"📁 Demo file saved to: {temp_file_path}")
    
    return temp_file_path


def demo_jira_csv_manager(ticket_id: str, products: List[str], has_existing_csv: bool = True):
    """
    Demonstrate the complete Jira CSV management workflow.
    
    Args:
        ticket_id: Jira ticket ID
        products: List of products to add
        has_existing_csv: Whether to simulate existing CSV
    """
    print(f"🚀 Demo: Processing ticket {ticket_id} with products: {products}")
    print("=" * 70)
    
    # Step 1: Download existing CSV (simulated)
    existing_rows = simulate_csv_download(ticket_id, has_existing_csv)
    
    # Step 2: Create new CSV content
    print(f"✏️  Adding {len(products)} new products to CSV...")
    csv_content = create_csv_content(existing_rows, products)
    
    # Step 3: Upload to ticket (simulated)
    temp_file = simulate_csv_upload(ticket_id, csv_content)
    
    # Step 4: Show the result
    print("\n📋 Final CSV content:")
    print("-" * 30)
    print(csv_content)
    
    print(f"🎉 Demo completed! Check the result in: {temp_file}")
    print("=" * 70)
    return temp_file


def main():
    """Run demonstration scenarios."""
    print("🔧 Jira CSV Manager - Demo Mode")
    print("This demo shows how the script works without requiring Jira credentials.\n")
    
    # Demo 1: Adding to existing CSV
    print("DEMO 1: Adding products to existing CSV")
    temp_file1 = demo_jira_csv_manager(
        ticket_id="PROJ-123", 
        products=["New Product X", "New Product Y", "New Product Z"],
        has_existing_csv=True
    )
    
    print("\n" + "="*70 + "\n")
    
    # Demo 2: Creating new CSV
    print("DEMO 2: Creating new CSV (no existing file)")
    temp_file2 = demo_jira_csv_manager(
        ticket_id="PROJ-456", 
        products=["First Product", "Second Product"],
        has_existing_csv=False
    )
    
    print("\n" + "="*70 + "\n")
    
    # Demo 3: Adding single product
    print("DEMO 3: Adding single product to existing CSV")
    temp_file3 = demo_jira_csv_manager(
        ticket_id="PROJ-789", 
        products=["Single New Product"],
        has_existing_csv=True
    )
    
    print(f"\n📁 Demo files created:")
    print(f"   - {temp_file1}")
    print(f"   - {temp_file2}")
    print(f"   - {temp_file3}")
    print(f"\n💡 To use with real Jira, set up your .env file and run:")
    print(f"   python jira_csv_manager.py TICKET-ID 'Product Name'")


if __name__ == "__main__":
    main()