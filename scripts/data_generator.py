"""Script containing the function to generate challenging test data for the moderation pipeline."""

from typing import List, Dict

def generate_test_data(num_entries: int = 5) -> List[Dict]:
    """
    Generates a list of dictionaries containing intentionally messy and challenging test data
    for content moderation testing.

    The data includes varying lengths, mixed cases, and different types.

    Args:
        num_entries: The number of test entries to generate.

    Returns:
        A list of dictionaries, each representing a data entry.
    """
    data = []
    
    # Pre-defined challenging entries to ensure all rules are tested
    test_cases = [
        # 1. Short Content + Negative Keywords (Likely BLOCK/WARN)
        {'id': 101, 'text': 'This is bad and fail!', 'topic': 'General', 'date': '2024-10-15'},
        # 2. Political + Old Date (Likely BLOCK/WARN)
        {'id': 102, 'text': 'Major policy changes required.', 'topic': 'Political', 'date': '2023-01-01'},
        # 3. Long, Safe Content (Likely PASS)
        {'id': 103, 'text': 'This is a very long and descriptive piece of content that should pass all checks with flying colors.', 'topic': 'Tech', 'date': '2026-09-01'},
        # 4. Short, Neutral Content (Likely PASS)
        {'id': 104, 'text': 'Okay.', 'topic': 'General', 'date': '2026-09-07'},
        # 5. Mixed case, borderline topic (Test variable score)
        {'id': 105, 'text': 'Amazing success report.', 'topic': 'Science', 'date': '2026-05-01'},
        # 6. Example of a very old date to test the 6-month logic
        {'id': 106, 'text': 'Global economy failing badly.', 'topic': 'Political', 'date': '2023-11-15'}
    ]
    
    # Use the first 'num_entries' cases, or cycle if num_entries > len(test_cases)
    for i in range(num_entries):
        data.append(test_cases[i % len(test_cases)])
        
    return data

if __name__ == '__main__':
    test_data = generate_test_data(5)
    print("--- Generated Test Data (data_generator.py) ---")
    for entry in test_data:
        print(entry)