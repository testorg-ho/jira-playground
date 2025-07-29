#!/usr/bin/env python3
"""
Usage examples for Jira CSV Manager.

This file contains examples of how to use the jira_csv_manager.py script.
"""

# Example 1: Basic usage with single product
# python jira_csv_manager.py PROJ-123 "New Product"

# Example 2: Adding multiple products at once
# python jira_csv_manager.py PROJ-456 "Product A" "Product B" "Product C"

# Example 3: Adding products with spaces and special characters
# python jira_csv_manager.py TICKET-789 "Complex Product Name (v2.0)" "Product with & symbols"

# Example 4: Real-world scenario
# python jira_csv_manager.py SUPPORT-101 "iPhone 15 Pro" "Samsung Galaxy S24" "Google Pixel 8"

"""
Before running these examples, make sure you have:

1. Installed dependencies:
   pip install -r requirements.txt

2. Set up your .env file with Jira credentials:
   cp .env.example .env
   # Edit .env with your actual Jira server, email, and API token

3. Verify you have access to the Jira tickets you're trying to modify

The script will:
- Connect to your Jira instance
- Look for existing "items.csv" in the ticket
- Add your products to the CSV (or create new if none exists)
- Upload the modified CSV back to the ticket
- Remove the old CSV attachment if it existed

CSV Format:
Number,Item Name
1,First Product
2,Second Product
...
"""

if __name__ == "__main__":
    print("This file contains usage examples for jira_csv_manager.py")
    print("See the comments in this file for command examples.")
    print("\nTo run the actual script, use:")
    print("python jira_csv_manager.py <ticket_id> <product1> [product2] ...")
    print("\nTo see a demo without Jira credentials:")
    print("python demo.py")