# Jira CSV Manager

A Python script that manages CSV attachments in Jira tickets. It can download existing "items.csv" files from tickets, add new products to them, and upload the modified CSV back to the ticket.

## Features

- **Download CSV attachments**: Automatically finds and downloads "items.csv" from Jira tickets
- **Smart CSV handling**: Maintains existing data structure and numbering
- **Add new products**: Adds products to existing CSV or creates new CSV if none exists
- **Automatic upload**: Replaces old CSV attachment with updated version
- **Error handling**: Comprehensive error handling and logging

## Prerequisites

- Python 3.7 or higher
- Jira account with API access
- API token for authentication

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd jira-playground
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure your Jira credentials:
   ```bash
   cp .env.example .env
   # Edit .env with your Jira details
   ```

## Configuration

Create a `.env` file with your Jira credentials:

```env
JIRA_SERVER=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token-here
```

### Getting Your Jira API Token

1. Go to [https://id.atlassian.com/manage-profile/security/api-tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
2. Click "Create API token"
3. Give it a name and copy the token
4. Use this token in your `.env` file

## Usage

```bash
python jira_csv_manager.py <ticket_id> <product1> [product2] [product3] ...
```

### Examples

Add single product to ticket:
```bash
python jira_csv_manager.py PROJ-123 "New Product"
```

Add multiple products:
```bash
python jira_csv_manager.py PROJ-123 "Product A" "Product B" "Product C"
```

## CSV Structure

The script expects/creates CSV files with the following structure:

| Number | Item Name |
|--------|-----------|
| 1      | Product A |
| 2      | Product B |
| 3      | Product C |

## How It Works

1. **Connect to Jira**: Uses your credentials to authenticate with Jira API
2. **Find existing CSV**: Looks for "items.csv" attachment in the specified ticket
3. **Download and parse**: If found, downloads and parses the existing CSV
4. **Add new products**: Adds your specified products with incremental numbering
5. **Upload**: Removes old CSV (if exists) and uploads the new version

## Error Handling

The script handles common scenarios:

- **No existing CSV**: Creates a new CSV with proper headers
- **Missing credentials**: Clear error message about environment setup
- **Ticket not found**: Reports if the ticket ID is invalid
- **Network issues**: Handles connection problems gracefully
- **Permission issues**: Reports if you don't have access to the ticket

## Testing

Test the CSV functionality without Jira:
```bash
python test_csv_simple.py
```

## Troubleshooting

### "Missing Jira credentials" error
- Check that your `.env` file exists and has the correct variables
- Verify your API token is correct

### "Failed to connect to Jira" error
- Check your Jira server URL (should include https://)
- Verify your email and API token are correct
- Ensure you have API access enabled

### "Permission denied" or ticket access errors
- Verify you have access to the specified ticket
- Check that the ticket ID format is correct (e.g., PROJ-123)

## Security Notes

- Never commit your `.env` file to version control
- Keep your API token secure and rotate it regularly
- Use project-specific tokens when possible