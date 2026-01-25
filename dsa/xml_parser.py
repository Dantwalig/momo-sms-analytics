"""
XML parsing module for MoMo SMS data.
Converts XML SMS records to JSON format.
"""

import xml.etree.ElementTree as ET
from typing import List, Dict, Any
import json


def parse_xml_file(file_path: str) -> List[Dict[str, Any]]:
    """
    Parse XML file and extract SMS transaction data.
    
    Args:
        file_path: Path to the XML file
        
    Returns:
        List of dictionaries containing parsed transaction data
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        
        transactions = []
        for sms in root.findall('sms'):
            transaction = extract_transaction_fields(sms)
            if transaction:
                transactions.append(transaction)
        
        return transactions
    except ET.ParseError as e:
        raise ValueError(f"Error parsing XML file: {e}")
    except FileNotFoundError:
        raise FileNotFoundError(f"XML file not found: {file_path}")


def extract_transaction_fields(element: ET.Element) -> Dict[str, Any]:
    """
    Extract transaction fields from an XML element.
    
    Args:
        element: XML element containing SMS transaction data
        
    Returns:
        Dictionary with transaction fields
    """
    try:
        # Extract all attributes from the SMS element
        transaction = {
            'protocol': element.get('protocol', ''),
            'address': element.get('address', ''),
            'date': element.get('date', ''),
            'type': element.get('type', ''),
            'subject': element.get('subject', ''),
            'body': element.get('body', ''),
            'toa': element.get('toa', ''),
            'sc_toa': element.get('sc_toa', ''),
            'service_center': element.get('service_center', ''),
            'read': element.get('read', ''),
            'status': element.get('status', ''),
            'locked': element.get('locked', ''),
            'date_sent': element.get('date_sent', ''),
            'sub_id': element.get('sub_id', ''),
            'readable_date': element.get('readable_date', ''),
            'contact_name': element.get('contact_name', '')
        }
        
        return transaction
    except Exception as e:
        print(f"Error extracting transaction fields: {e}")
        return None


def convert_to_json(transactions: List[Dict[str, Any]], output_path: str = None) -> str:
    """
    Convert list of transactions to JSON format.
    
    Args:
        transactions: List of transaction dictionaries
        output_path: Optional path to save JSON file
        
    Returns:
        JSON string representation of transactions
    """
    json_data = json.dumps(transactions, indent=2, ensure_ascii=False)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(json_data)
    
    return json_data


if __name__ == '__main__':
    # Example usage
    transactions = parse_xml_file('modified_sms_v2.xml')
    print(f"Parsed {len(transactions)} transactions")
    print(f"First transaction: {json.dumps(transactions[0] if transactions else {}, indent=2)}")
