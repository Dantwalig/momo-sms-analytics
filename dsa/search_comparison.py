"""
Data Structures and Algorithms comparison module.
Compares linear search vs dictionary lookup performance.
"""

import time
from typing import List, Dict, Any, Optional, Tuple
from dsa.xml_parser import parse_xml_file


def linear_search(transactions: List[Dict[str, Any]], target_id: str) -> Optional[Dict[str, Any]]:
    """
    Linear search through list to find transaction by ID.
    Time Complexity: O(n)
    
    Args:
        transactions: List of transaction dictionaries
        target_id: Transaction ID to search for (index-based for XML data)
        
    Returns:
        Transaction dictionary if found, None otherwise
    """
    try:
        target_idx = int(target_id)
        if 0 <= target_idx < len(transactions):
            return transactions[target_idx]
    except (ValueError, IndexError):
        pass
    
    # Fallback: search by any ID-like field if present
    for transaction in transactions:
        if str(transaction.get('transaction_id', '')) == str(target_id):
            return transaction
    return None


def dictionary_lookup(transactions_dict: Dict[str, Dict[str, Any]], target_id: str) -> Optional[Dict[str, Any]]:
    """
    Dictionary lookup to find transaction by ID.
    Time Complexity: O(1)
    
    Args:
        transactions_dict: Dictionary with transaction IDs as keys
        target_id: Transaction ID to search for
        
    Returns:
        Transaction dictionary if found, None otherwise
    """
    return transactions_dict.get(str(target_id))


def build_dictionary(transactions: List[Dict[str, Any]], id_field: str = None) -> Dict[str, Dict[str, Any]]:
    """
    Build dictionary from list of transactions for O(1) lookup.
    
    Args:
        transactions: List of transaction dictionaries
        id_field: Field name to use as dictionary key (if None, uses index)
        
    Returns:
        Dictionary with transaction IDs as keys
    """
    transactions_dict = {}
    for idx, transaction in enumerate(transactions):
        # Use index as key for XML parsed data (no transaction_id field)
        if id_field and id_field in transaction:
            key = str(transaction[id_field])
        else:
            key = str(idx)
        transactions_dict[key] = transaction
    return transactions_dict


def compare_search_methods(transactions: List[Dict[str, Any]], 
                          search_ids: List[str],
                          iterations: int = 100) -> Dict[str, Any]:
    """
    Compare performance of linear search vs dictionary lookup.
    
    Args:
        transactions: List of transaction dictionaries
        search_ids: List of IDs to search for
        iterations: Number of iterations to average over
        
    Returns:
        Dictionary with performance metrics and comparison
    """
    # Build dictionary for lookup
    transactions_dict = build_dictionary(transactions)
    
    # Time linear search
    linear_times = []
    for _ in range(iterations):
        start = time.perf_counter()
        for search_id in search_ids:
            linear_search(transactions, search_id)
        end = time.perf_counter()
        linear_times.append(end - start)
    
    avg_linear_time = sum(linear_times) / len(linear_times)
    
    # Time dictionary lookup
    dict_times = []
    for _ in range(iterations):
        start = time.perf_counter()
        for search_id in search_ids:
            dictionary_lookup(transactions_dict, search_id)
        end = time.perf_counter()
        dict_times.append(end - start)
    
    avg_dict_time = sum(dict_times) / len(dict_times)
    
    # Calculate speedup
    speedup = avg_linear_time / avg_dict_time if avg_dict_time > 0 else float('inf')
    
    return {
        'num_transactions': len(transactions),
        'num_searches': len(search_ids),
        'iterations': iterations,
        'linear_search': {
            'avg_time_seconds': avg_linear_time,
            'avg_time_ms': avg_linear_time * 1000,
            'time_complexity': 'O(n)'
        },
        'dictionary_lookup': {
            'avg_time_seconds': avg_dict_time,
            'avg_time_ms': avg_dict_time * 1000,
            'time_complexity': 'O(1)'
        },
        'speedup': speedup,
        'reflection': {
            'why_dictionary_faster': (
                "Dictionary lookup is faster because it uses hash-based indexing, "
                "providing O(1) average-case time complexity. Linear search must "
                "iterate through the entire list until finding the target, resulting "
                "in O(n) time complexity where n is the number of transactions."
            ),
            'alternative_structures': (
                "Alternative data structures that could improve search efficiency:\n"
                "1. Binary Search Tree (BST): O(log n) search time for sorted data\n"
                "2. B-Tree: Efficient for large datasets with O(log n) search\n"
                "3. Hash Table (Dictionary): Already using - best for exact matches\n"
                "4. Trie: Useful for prefix-based searches\n"
                "5. Indexed database: For persistent storage with optimized queries"
            )
        }
    }


def run_comparison(xml_file_path: str = 'modified_sms_v2.xml', 
                   num_test_records: int = 20) -> Dict[str, Any]:
    """
    Run comparison test with parsed XML data.
    
    Args:
        xml_file_path: Path to XML file
        num_test_records: Number of records to test with
        
    Returns:
        Comparison results dictionary
    """
    print(f"Parsing XML file: {xml_file_path}")
    transactions = parse_xml_file(xml_file_path)
    
    # Limit to specified number of records for testing
    test_transactions = transactions[:num_test_records]
    
    # Generate search IDs (use indices as IDs for testing)
    search_ids = [str(i) for i in range(min(10, len(test_transactions)))]
    
    print(f"Testing with {len(test_transactions)} transactions")
    print(f"Searching for {len(search_ids)} IDs")
    
    results = compare_search_methods(test_transactions, search_ids)
    
    return results


if __name__ == '__main__':
    # Run comparison
    results = run_comparison()
    
    print("\n" + "="*60)
    print("DSA COMPARISON RESULTS")
    print("="*60)
    print(f"\nNumber of transactions: {results['num_transactions']}")
    print(f"Number of searches: {results['num_searches']}")
    print(f"Iterations: {results['iterations']}")
    
    print("\n--- Linear Search ---")
    print(f"Average time: {results['linear_search']['avg_time_ms']:.4f} ms")
    print(f"Time complexity: {results['linear_search']['time_complexity']}")
    
    print("\n--- Dictionary Lookup ---")
    print(f"Average time: {results['dictionary_lookup']['avg_time_ms']:.4f} ms")
    print(f"Time complexity: {results['dictionary_lookup']['time_complexity']}")
    
    print(f"\n--- Speedup ---")
    print(f"Dictionary lookup is {results['speedup']:.2f}x faster")
    
    print("\n--- Reflection ---")
    print(results['reflection']['why_dictionary_faster'])
    print("\n" + results['reflection']['alternative_structures'])
