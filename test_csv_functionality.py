#!/usr/bin/env python3
"""
Test script for JiraCSVManager CSV functionality.

This script tests the CSV creation and manipulation logic without requiring Jira credentials.
"""

import io
import csv
from jira_csv_manager import JiraCSVManager


def test_csv_creation():
    """Test CSV creation functionality."""
    print("Testing CSV creation functionality...")
    
    # Create a mock manager instance (we'll only test CSV methods)
    class MockJiraCSVManager(JiraCSVManager):
        def __init__(self):
            # Skip Jira initialization for testing
            pass
    
    manager = MockJiraCSVManager()
    
    # Test 1: Create new CSV from scratch
    print("\n1. Testing new CSV creation:")
    products = ["Product A", "Product B", "Product C"]
    csv_content = manager.create_csv_content(None, products)
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
    csv_content = manager.create_csv_content(existing_rows, new_products)
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
    csv_content = manager.create_csv_content(existing_rows_with_gaps, new_products)
    print("Generated CSV:")
    print(csv_content)
    
    # Verify the CSV content - should start from highest number + 1
    csv_reader = csv.reader(io.StringIO(csv_content))
    rows = list(csv_reader)
    assert len(rows) == 5  # Header + 3 existing + 1 new
    assert rows[4] == ['6', 'New Product']  # Should be 5 + 1 = 6
    print("✅ Gaps in numbering test passed")
    
    print("\n🎉 All CSV functionality tests passed!")


if __name__ == "__main__":
    test_csv_creation()