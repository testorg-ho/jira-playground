#!/usr/bin/env python3
"""
Simplified CSV functionality test without external dependencies.

This script tests the core CSV logic that will be used in the Jira script.
"""

import csv
import io
from typing import List, Optional


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


def test_csv_functionality():
    """Test CSV creation functionality."""
    print("Testing CSV creation functionality...")
    
    # Test 1: Create new CSV from scratch
    print("\n1. Testing new CSV creation:")
    products = ["Product A", "Product B", "Product C"]
    csv_content = create_csv_content(None, products)
    print("Generated CSV:")
    print(csv_content)
    
    # Verify the CSV content
    csv_reader = csv.reader(io.StringIO(csv_content))
    rows = list(csv_reader)
    assert len(rows) == 4  # Header + 3 products
    assert rows[0] == ['Number', 'Item Name']
    assert rows[1] == ['1', 'Product A']
    assert rows[2] == ['2', 'Product B']
    assert rows[3] == ['3', 'Product C']
    print("✅ New CSV creation test passed")
    
    # Test 2: Add to existing CSV
    print("\n2. Testing adding to existing CSV:")
    existing_rows = [
        ['Number', 'Item Name'],
        ['1', 'Existing Product 1'],
        ['2', 'Existing Product 2']
    ]
    new_products = ["New Product A", "New Product B"]
    csv_content = create_csv_content(existing_rows, new_products)
    print("Generated CSV:")
    print(csv_content)
    
    # Verify the CSV content
    csv_reader = csv.reader(io.StringIO(csv_content))
    rows = list(csv_reader)
    assert len(rows) == 5  # Header + 2 existing + 2 new
    assert rows[0] == ['Number', 'Item Name']
    assert rows[1] == ['1', 'Existing Product 1']
    assert rows[2] == ['2', 'Existing Product 2']
    assert rows[3] == ['3', 'New Product A']
    assert rows[4] == ['4', 'New Product B']
    print("✅ Adding to existing CSV test passed")
    
    # Test 3: Handle gaps in numbering
    print("\n3. Testing with gaps in existing numbering:")
    existing_rows_with_gaps = [
        ['Number', 'Item Name'],
        ['1', 'Product 1'],
        ['5', 'Product 5'],
        ['3', 'Product 3']
    ]
    new_products = ["New Product"]
    csv_content = create_csv_content(existing_rows_with_gaps, new_products)
    print("Generated CSV:")
    print(csv_content)
    
    # Verify the CSV content - should start from highest number + 1
    csv_reader = csv.reader(io.StringIO(csv_content))
    rows = list(csv_reader)
    assert len(rows) == 5  # Header + 3 existing + 1 new
    assert rows[4] == ['6', 'New Product']  # Should be 5 + 1 = 6
    print("✅ Gaps in numbering test passed")
    
    # Test 4: Empty products list
    print("\n4. Testing with empty products list:")
    existing_rows = [
        ['Number', 'Item Name'],
        ['1', 'Existing Product']
    ]
    empty_products = []
    csv_content = create_csv_content(existing_rows, empty_products)
    print("Generated CSV:")
    print(csv_content)
    
    # Verify the CSV content - should just return existing data
    csv_reader = csv.reader(io.StringIO(csv_content))
    rows = list(csv_reader)
    assert len(rows) == 2  # Header + 1 existing
    assert rows[0] == ['Number', 'Item Name']
    assert rows[1] == ['1', 'Existing Product']
    print("✅ Empty products list test passed")
    
    print("\n🎉 All CSV functionality tests passed!")


if __name__ == "__main__":
    test_csv_functionality()