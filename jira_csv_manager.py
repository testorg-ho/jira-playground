#!/usr/bin/env python3
"""
Jira CSV Manager

This script manages CSV attachments in Jira tickets. It can:
1. Download existing "items.csv" from a Jira ticket (if exists)
2. Add new products to the CSV or create a new one
3. Upload the modified CSV back to the ticket

Usage:
    python jira_csv_manager.py <ticket_id> <product1> [product2] [product3] ...

Example:
    python jira_csv_manager.py PROJ-123 "Product A" "Product B" "Product C"
"""

import csv
import io
import logging
import os
import sys
import tempfile
from typing import List, Optional, Tuple

from jira import JIRA
from dotenv import load_dotenv


# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class JiraCSVManager:
    """Manages CSV attachments in Jira tickets."""
    
    def __init__(self):
        """Initialize Jira connection."""
        self.jira_server = os.getenv('JIRA_SERVER')
        self.jira_email = os.getenv('JIRA_EMAIL')
        self.jira_token = os.getenv('JIRA_API_TOKEN')
        
        if not all([self.jira_server, self.jira_email, self.jira_token]):
            raise ValueError("Missing Jira credentials. Please set JIRA_SERVER, JIRA_EMAIL, and JIRA_API_TOKEN environment variables.")
        
        try:
            self.jira = JIRA(
                server=self.jira_server,
                basic_auth=(self.jira_email, self.jira_token)
            )
            logger.info("Successfully connected to Jira")
        except Exception as e:
            logger.error(f"Failed to connect to Jira: {e}")
            raise
    
    def download_items_csv(self, ticket_id: str) -> Optional[List[List[str]]]:
        """
        Download items.csv attachment from Jira ticket if it exists.
        
        Args:
            ticket_id: Jira ticket ID (e.g., "PROJ-123")
            
        Returns:
            List of CSV rows as lists, or None if no items.csv found
        """
        try:
            issue = self.jira.issue(ticket_id)
            logger.info(f"Found ticket: {issue.key}")
            
            # Look for items.csv attachment
            for attachment in issue.fields.attachment:
                if attachment.filename.lower() == 'items.csv':
                    logger.info(f"Found items.csv attachment: {attachment.filename}")
                    
                    # Download the attachment content
                    content = attachment.get()
                    csv_content = content.decode('utf-8')
                    
                    # Parse CSV
                    csv_reader = csv.reader(io.StringIO(csv_content))
                    rows = list(csv_reader)
                    
                    logger.info(f"Downloaded CSV with {len(rows)} rows")
                    return rows
            
            logger.info("No items.csv attachment found")
            return None
            
        except Exception as e:
            logger.error(f"Error downloading CSV from ticket {ticket_id}: {e}")
            raise
    
    def create_csv_content(self, existing_rows: Optional[List[List[str]]], products: List[str]) -> str:
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
        
        logger.info(f"Created CSV content with {len(products)} new products")
        return csv_content
    
    def upload_csv_to_ticket(self, ticket_id: str, csv_content: str) -> None:
        """
        Upload CSV content to Jira ticket, replacing existing items.csv if present.
        
        Args:
            ticket_id: Jira ticket ID
            csv_content: CSV content as string
        """
        try:
            issue = self.jira.issue(ticket_id)
            
            # Remove existing items.csv attachments
            for attachment in issue.fields.attachment:
                if attachment.filename.lower() == 'items.csv':
                    logger.info(f"Removing existing attachment: {attachment.filename}")
                    attachment.delete()
            
            # Create temporary file for upload
            with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as temp_file:
                temp_file.write(csv_content)
                temp_file_path = temp_file.name
            
            try:
                # Upload new CSV
                with open(temp_file_path, 'rb') as f:
                    self.jira.add_attachment(issue=issue, attachment=f, filename='items.csv')
                logger.info("Successfully uploaded new items.csv")
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)
                
        except Exception as e:
            logger.error(f"Error uploading CSV to ticket {ticket_id}: {e}")
            raise
    
    def process_ticket(self, ticket_id: str, products: List[str]) -> None:
        """
        Main method to process a ticket: download CSV, add products, upload back.
        
        Args:
            ticket_id: Jira ticket ID
            products: List of products to add
        """
        logger.info(f"Processing ticket {ticket_id} with {len(products)} products")
        
        # Download existing CSV
        existing_rows = self.download_items_csv(ticket_id)
        
        # Create new CSV content
        csv_content = self.create_csv_content(existing_rows, products)
        
        # Upload to ticket
        self.upload_csv_to_ticket(ticket_id, csv_content)
        
        logger.info(f"Successfully processed ticket {ticket_id}")


def main():
    """Main entry point."""
    if len(sys.argv) < 3:
        print("Usage: python jira_csv_manager.py <ticket_id> <product1> [product2] [product3] ...")
        print("Example: python jira_csv_manager.py PROJ-123 'Product A' 'Product B'")
        sys.exit(1)
    
    ticket_id = sys.argv[1]
    products = sys.argv[2:]
    
    try:
        manager = JiraCSVManager()
        manager.process_ticket(ticket_id, products)
        print(f"✅ Successfully updated {ticket_id} with {len(products)} products")
    except Exception as e:
        logger.error(f"Failed to process ticket: {e}")
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()